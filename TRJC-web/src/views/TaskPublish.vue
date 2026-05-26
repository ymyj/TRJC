<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">{{ isEditMode ? '编辑任务' : '任务发布' }}</h1>
    </div>

    <div class="form-card">
      <div class="form-row">
        <div class="form-item">
          <label class="form-label">任务名称<span class="required">*</span></label>
          <input type="text" class="form-input" placeholder="请输入任务名称" v-model="form.name">
          <span class="form-hint"></span>
        </div>
        <div class="form-item">
          <label class="form-label">任务类型<span class="required">*</span></label>
          <select class="form-select" v-model="form.type">
            <option value="">请选择任务类型</option>
            <option value="routine">常规监测</option>
            <option value="supplement">补充鉴定</option>
            <option value="special">专项监测</option>
            <option value="census">普查任务</option>
            <option value="check">质量核查</option>
          </select>
          <span class="form-hint"></span>
        </div>
      </div>
      <div class="form-row">
        <div class="form-item">
          <label class="form-label">计划开始时间</label>
          <input type="date" class="form-input" v-model="form.startDate" @change="handleDateChange">
        </div>
        <div class="form-item">
          <label class="form-label">项目负责人<span class="required">*</span></label>
          <select class="form-select" v-model="form.personId" @change="handlePersonChange">
            <option value="">请选择负责人</option>
            <option v-for="person in personnelList" :key="person.ID" :value="person.ID">{{ person.XM }}</option>
          </select>
        </div>
      </div>

      <div class="form-row">
        <div class="form-item">
          <label class="form-label">联系电话</label>
          <input type="text" class="form-input" placeholder="自动填充" v-model="form.phone" readonly>
        </div>
      </div>

      <div class="form-row">
        <div class="form-item" style="flex: 2;">
          <label class="form-label">任务描述</label>
          <textarea class="form-textarea" placeholder="请详细描述任务背景、目的和注意事项..." v-model="form.description"></textarea>
          <span class="form-hint">最多支持输入2000个字符</span>
        </div>
      </div>

      <div class="form-row">
        <div class="form-item" style="flex: 2;">
          <label class="form-label">相关附件</label>
          <div class="upload-section">
            <p class="upload-tip">支持添加最多20个附件</p>
            <div class="upload-area" @click="triggerUpload" @dragover.prevent @drop.prevent="handleDrop">
              <div class="upload-icon">↑</div>
              <p class="upload-text">拖拽文件到此处或 <span class="upload-link">点击选择文件</span></p>
              <p class="upload-hint">支持PDF、Word、Excel、图片格式，单个文件不超过50MB</p>
              <button class="upload-btn" type="button">选择文件</button>
              <input ref="fileInput" type="file" class="file-input" multiple @change="handleUpload" accept=".pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png,.gif">
            </div>
            <div v-if="uploadedFiles.length > 0" class="file-list">
              <div v-for="(file, index) in uploadedFiles" :key="index" class="file-item">
                <span class="file-name">{{ file.name }}</span>
                <span class="file-size">{{ formatFileSize(file.size) }}</span>
                <button class="file-remove" @click="removeFile(index)">删除</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 地块选择区域 -->
      <div class="form-row">
        <div class="form-item" style="flex: 2;">
          <div class="land-section">
            <label class="form-label"><span class="required">*</span>地块选择</label>
            <button class="btn btn-primary" @click="handleSelectLand">选择</button>
          </div>
          <table class="data-table">
            <thead>
              <tr>
                <th>图斑编号</th>
                <th>所属单元</th>
                <th>图斑面积（㎡）</th>
                <th>所属区划</th>
                <th>经度</th>
                <th>纬度</th>
                <th>创建时间</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(land, index) in selectedLands" :key="index">
                <td>{{ land.TBH }}</td>
                <td>{{ land.SSDY }}</td>
                <td>{{ land.TBMJ }}</td>
                <td>{{ land.SSQH }}</td>
                <td>{{ land.JD }}</td>
                <td>{{ land.WD }}</td>
                <td>{{ land.CJSJ }}</td>
                <td>
                  <span class="action-link" @click="deleteLand(index)">删除</span>
                </td>
              </tr>
              <tr v-if="selectedLands.length === 0">
                <td colspan="8" class="empty-cell">暂无数据</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="form-actions">
        <button class="btn btn-default btn-large" @click="handleCancel">取消</button>
        <button class="btn btn-primary btn-large" @click="handlePublish">{{ isEditMode ? '保存修改' : '发布任务' }}</button>
      </div>
    </div>

    <!-- 地块选择弹窗 -->
    <div v-if="showLandModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="modal-title">地块选择</h3>
          <button class="modal-close" @click="closeModal">×</button>
        </div>
        <div class="modal-body">
          <!-- 查询条件 -->
          <div class="modal-filter">
            <div class="filter-row">
              <div class="filter-item">
                <label class="filter-label">图斑编号</label>
                <input type="text" class="form-input" placeholder="请输入图斑编号" v-model="modalFilter.code">
              </div>
              <div class="filter-item">
                <label class="filter-label">所属单元</label>
                <input type="text" class="form-input" placeholder="请输入所属单元" v-model="modalFilter.unit">
              </div>
              <div class="filter-item">
                <label class="filter-label">所属区划</label>
                <select class="form-select" v-model="modalFilter.district">
                  <option value="">全部区划</option>
                  <option v-for="option in plotDistrictOptions" :key="option.value" :value="option.value">{{ option.label }}</option>
                </select>
              </div>
            </div>
            <div class="filter-actions">
              <button class="btn btn-default" @click="resetModalFilter">重置</button>
              <button class="btn btn-primary" @click="queryModalData">查询</button>
            </div>
          </div>

          <!-- 数据表格 -->
          <table class="modal-table">
            <thead>
              <tr>
                <th style="width: 40px;"><input type="checkbox" class="checkbox" v-model="selectAllModal"></th>
                <th>图斑编号</th>
                <th>所属单元</th>
                <th>图斑面积（㎡）</th>
                <th>所属区划</th>
                <th>经度</th>
                <th>纬度</th>
                <th>创建时间</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="land in modalLandList" :key="land.ID" @click="toggleSelect(land)" class="clickable-row">
                <td><input type="checkbox" class="checkbox" v-model="land.selected" @click.stop></td>
                <td>{{ land.TBH }}</td>
                <td>{{ land.SSDY }}</td>
                <td>{{ land.TBMJ }}</td>
                <td>{{ land.SSQH }}</td>
                <td>{{ land.JD }}</td>
                <td>{{ land.WD }}</td>
                <td>{{ land.CJSJ }}</td>
              </tr>
              <tr v-if="modalLandList.length === 0">
                <td colspan="8" class="empty-cell">暂无数据</td>
              </tr>
            </tbody>
          </table>

          <!-- 分页 -->
          <div class="modal-pagination">
            <span class="pagination-info">显示 {{ modalPagination.start }} 到 {{ modalPagination.end }} 条，共 {{ modalPagination.total }} 条记录</span>
            <div class="pagination">
              <button class="page-btn" :disabled="modalPagination.current === 1" @click="changeModalPage(modalPagination.current - 1)">&lt;</button>
              <button 
                v-for="page in modalPagination.pages" 
                :key="page" 
                class="page-btn" 
                :class="{ active: page === modalPagination.current }"
                @click="changeModalPage(page)"
              >{{ page }}</button>
              <button class="page-btn" :disabled="modalPagination.current === modalPagination.totalPages" @click="changeModalPage(modalPagination.current + 1)">&gt;</button>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-default" @click="closeModal">取消</button>
          <button class="btn btn-primary" @click="confirmSelect">确定</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getPlotList, getPersonnelForAssignment, createTask, getTaskDetail, updateTask, uploadAttachment, getAttachments, deleteAttachment } from '../api'

const router = useRouter()
const route = useRoute()

const isEditMode = computed(() => !!route.query.editId)

const form = reactive({
  name: '',
  type: '',
  startTime: '',
  startDate: '',
  personId: '',
  phone: '',
  description: ''
})

const selectedLands = ref([])
const fileInput = ref(null)
const uploading = ref(false)
const uploadedFiles = ref([])

const triggerUpload = () => {
  fileInput.value.click()
}

const handleDateChange = () => {
  if (form.startDate) {
    form.startTime = form.startDate + ' 09:00:00'
  } else {
    form.startTime = ''
  }
}

const personnelList = ref([])
const plotList = ref([])
const plotDistrictOptions = ref([])

// 弹窗相关
const showLandModal = ref(false)
const modalFilter = reactive({
  code: '',
  unit: '',
  district: ''
})

const modalLandList = ref([])

const modalPagination = reactive({
  current: 1,
  total: 0,
  pageSize: 10,
  pages: [],
  get start() { return (this.current - 1) * this.pageSize + 1 },
  get end() { return Math.min(this.current * this.pageSize, this.total) },
  get totalPages() { return Math.ceil(this.total / this.pageSize) }
})

const selectAllModal = computed({
  get() {
    return modalLandList.value.length > 0 && modalLandList.value.every(item => item.selected)
  },
  set(value) {
    modalLandList.value.forEach(item => item.selected = value)
  }
})

const fetchPlotList = async () => {
  const res = await getPlotList({ page: 1, size: 100 })
  if (res.data.code === 200) {
    plotList.value = (res.data.data.list || []).map(item => ({
      ...item,
      selected: false
    }))
    const districts = [...new Set(plotList.value.map(p => p.SSQH).filter(Boolean))]
    plotDistrictOptions.value = districts.map(d => ({ value: d, label: d }))
    modalLandList.value = [...plotList.value]
    modalPagination.total = modalLandList.value.length
    updateModalPaginationPages()
  }
}

const fetchPersonnelList = async () => {
  const res = await getPersonnelForAssignment({ page: 1, size: 100 })
  if (res.data.code === 200) {
    personnelList.value = res.data.data.list || []
  }
}

const handlePersonChange = () => {
  const selectedPerson = personnelList.value.find(p => p.ID === form.personId)
  if (selectedPerson) {
    form.phone = selectedPerson.LXFS || ''
  } else {
    form.phone = ''
  }
}

const updateModalPaginationPages = () => {
  const totalPages = modalPagination.totalPages
  const pages = []
  for (let i = 1; i <= totalPages; i++) {
    if (i === 1 || i === totalPages || Math.abs(i - modalPagination.current) <= 2) {
      pages.push(i)
    }
  }
  modalPagination.pages = pages
}

const handleCancel = () => {
  router.push('/tasks')
}

const handlePublish = async () => {
  if (!form.name || !form.type || !form.personId) {
    alert('请填写必填项')
    return
  }
  if (selectedLands.value.length === 0) {
    alert('请选择地块')
    return
  }

  const selectedPerson = personnelList.value.find(p => p.ID === form.personId)
  const data = {
    RWMC: form.name,
    RWLX: form.type,
    SSQH: '',
    FZR: selectedPerson ? selectedPerson.XM : '',
    JHKSSJ: form.startTime,
    LXDH: form.phone,
    RWMS: form.description,
    plot_ids: selectedLands.value.map(land => land.ID)
  }

  let res
  if (isEditMode.value) {
    res = await updateTask(route.query.editId, data)
    if (res.data.code === 200) {
      alert('任务更新成功')
      router.push('/tasks')
    } else {
      alert('任务更新失败: ' + (res.data.message || '未知错误'))
    }
  } else {
    res = await createTask(data)
    if (res.data.code === 200) {
      alert('任务创建成功')
      router.push('/tasks')
    } else {
      alert('任务创建失败: ' + (res.data.message || '未知错误'))
    }
  }
}

const handleUpload = async (event) => {
  const files = event.target.files || []
  if (files.length === 0) return
  await processFiles(files)
  event.target.value = ''
}

const handleDrop = async (event) => {
  const files = event.dataTransfer.files || []
  if (files.length === 0) return
  await processFiles(files)
}

const processFiles = async (files) => {
  if (!form.ID) {
    alert('请先保存任务后再上传附件')
    return
  }

  if (uploadedFiles.value.length + files.length > 20) {
    alert('最多支持20个附件')
    return
  }

  uploading.value = true
  for (const file of files) {
    const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'image/jpeg', 'image/png', 'image/gif']
    if (!allowedTypes.includes(file.type)) {
      alert(`不支持的文件类型: ${file.name}`)
      continue
    }
    if (file.size > 50 * 1024 * 1024) {
      alert(`文件大小超过50MB限制: ${file.name}`)
      continue
    }
    try {
      const res = await uploadAttachment(form.ID, file)
      uploadedFiles.value.push({ id: res.data.data.ID, name: res.data.data.FILE_NAME, size: file.size })
    } catch (error) {
      alert(`上传失败: ${file.name}`)
    }
  }
  uploading.value = false
}

const removeFile = async (index) => {
  const file = uploadedFiles.value[index]
  if (!file.id) {
    uploadedFiles.value.splice(index, 1)
    return
  }
  try {
    await deleteAttachment(file.id)
    uploadedFiles.value.splice(index, 1)
  } catch (error) {
    alert('删除失败')
  }
}

const formatFileSize = (bytes) => {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
}

const handleSelectLand = () => {
  showLandModal.value = true
}

const closeModal = () => {
  showLandModal.value = false
}

const resetModalFilter = () => {
  modalFilter.code = ''
  modalFilter.unit = ''
  modalFilter.district = ''
  queryModalData()
}

const queryModalData = () => {
  let filtered = plotList.value
  if (modalFilter.code) {
    filtered = filtered.filter(item => item.TBH?.includes(modalFilter.code))
  }
  if (modalFilter.unit) {
    filtered = filtered.filter(item => item.SSDY?.includes(modalFilter.unit))
  }
  if (modalFilter.district) {
    filtered = filtered.filter(item => item.SSQH === modalFilter.district)
  }
  modalLandList.value = filtered.map(item => ({
    ...item,
    selected: selectedLands.value.some(s => s.ID === item.ID)
  }))
  modalPagination.total = modalLandList.value.length
  modalPagination.current = 1
  updateModalPaginationPages()
}

const changeModalPage = (page) => {
  if (page >= 1 && page <= modalPagination.totalPages) {
    modalPagination.current = page
  }
}

const toggleSelect = (land) => {
  land.selected = !land.selected
}

const confirmSelect = () => {
  const selected = modalLandList.value.filter(item => item.selected)
  selectedLands.value = selected
  closeModal()
}

const deleteLand = (index) => {
  selectedLands.value.splice(index, 1)
}

onMounted(async () => {
  await fetchPlotList()
  await fetchPersonnelList()

  if (isEditMode.value) {
    const res = await getTaskDetail(route.query.editId)
    if (res.data.code === 200) {
      const d = res.data.data
      form.ID = d.ID
      form.name = d.RWMC
      form.type = d.RWLX
      form.startDate = d.JHKSSJ ? d.JHKSSJ.split(' ')[0] : ''
      form.startTime = d.JHKSSJ
      form.description = d.RWMS || ''

      const person = personnelList.value.find(p => p.XM === d.FZR)
      if (person) {
        form.personId = person.ID
        form.phone = person.LXFS || ''
      }

      if (d.plots && d.plots.length > 0) {
        selectedLands.value = d.plots.map(p => ({
          ID: p.ID,
          TBH: p.TBH,
          SSDY: p.SSDY,
          TBMJ: p.TBMJ,
          SSQH: p.SSQH,
          JD: p.JD,
          WD: p.WD,
          CJSJ: p.CJSJ
        }))
      }

      const attRes = await getAttachments(route.query.editId)
      if (attRes.data.code === 200) {
        uploadedFiles.value = attRes.data.data.map(f => ({
          id: f.ID,
          name: f.FILE_NAME,
          size: f.FILE_SIZE
        }))
      }
    }
  }
})
</script>

<style scoped>
.page-header {
  margin-bottom: 24px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
}

.form-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 32px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.form-row {
  display: flex;
  gap: 24px;
  margin-bottom: 24px;
}

.form-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 14px;
  color: #262626;
  font-weight: 500;
}

.form-label .required {
  color: #f5222d;
  margin-right: 4px;
}

.form-hint {
  font-size: 12px;
  color: #8c8c8c;
  margin-top: 4px;
}

.upload-section {
  margin-top: 8px;
}

.upload-area {
  border: 1px dashed #d9d9d9;
  border-radius: 8px;
  padding: 40px;
  text-align: center;
  background-color: #fafafa;
  transition: all 0.3s;
  cursor: pointer;
}

.upload-area:hover {
  border-color: #1677ff;
  background-color: #f0f7ff;
}

.upload-icon {
  width: 48px;
  height: 48px;
  margin: 0 auto 16px;
  background-color: #f0f0f0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-icon svg {
  width: 24px;
  height: 24px;
  color: #8c8c8c;
}

.upload-icon {
  font-size: 24px;
  color: #8c8c8c;
}

.upload-text {
  font-size: 14px;
  color: #262626;
  margin-bottom: 8px;
}

.upload-hint {
  font-size: 12px;
  color: #8c8c8c;
  margin-bottom: 20px;
}

.upload-btn {
  display: block;
  margin: 0 auto;
  padding: 8px 24px;
  border: 1px solid #1677ff;
  border-radius: 6px;
  background-color: #1677ff;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.upload-btn:hover {
  background-color: #4096ff;
  border-color: #4096ff;
}

.file-input {
  display: none;
}

.file-list {
  margin-top: 16px;
}

.file-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  background-color: #fafafa;
  border-radius: 6px;
  margin-bottom: 8px;
}

.file-name {
  flex: 1;
  font-size: 14px;
  color: #262626;
}

.file-size {
  font-size: 12px;
  color: #8c8c8c;
  margin-right: 12px;
}

.file-remove {
  padding: 4px 12px;
  border: none;
  background-color: #ff4d4f;
  color: #fff;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

.file-remove:hover {
  background-color: #ff7875;
}

/* 地块选择区域 */
.land-section {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.land-section .form-label {
  margin-bottom: 0;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
}

.data-table th {
  background-color: #fafafa;
  padding: 12px 16px;
  text-align: center;
  font-size: 13px;
  font-weight: 500;
  color: #595959;
  border-bottom: 1px solid #f0f0f0;
  border-right: 1px solid #f0f0f0;
}

.data-table th:last-child {
  border-right: none;
}

.data-table td {
  padding: 12px 16px;
  font-size: 14px;
  color: #262626;
  border-bottom: 1px solid #f0f0f0;
  border-right: 1px solid #f0f0f0;
  text-align: center;
}

.data-table td:last-child {
  border-right: none;
}

.data-table tr:last-child td {
  border-bottom: none;
}

.empty-cell {
  text-align: center;
  color: #8c8c8c;
  padding: 40px;
}

.action-link {
  color: #1677ff;
  cursor: pointer;
  font-size: 14px;
}

.action-link:hover {
  text-decoration: underline;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 40px;
  padding-top: 24px;
  border-top: 1px solid #f0f0f0;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  border-radius: 8px;
  width: 900px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #f0f0f0;
}

.modal-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  color: #8c8c8c;
  cursor: pointer;
  line-height: 1;
}

.modal-close:hover {
  color: #595959;
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid #f0f0f0;
}

/* 弹窗内查询条件 */
.modal-filter {
  background-color: #f5f7fa;
  padding: 16px;
  border-radius: 6px;
  margin-bottom: 16px;
}

.modal-filter .filter-row {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.modal-filter .filter-row:last-child {
  margin-bottom: 0;
}

.modal-filter .filter-item {
  flex: 1;
}

.modal-filter .filter-label {
  font-size: 13px;
  color: #595959;
  margin-bottom: 6px;
  display: block;
}

.modal-filter .filter-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

/* 弹窗内表格 */
.modal-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #f0f0f0;
  margin-bottom: 16px;
}

.modal-table th {
  background-color: #fafafa;
  padding: 12px;
  text-align: center;
  font-size: 13px;
  font-weight: 500;
  color: #595959;
  border-bottom: 1px solid #f0f0f0;
  border-right: 1px solid #f0f0f0;
}

.modal-table th:last-child {
  border-right: none;
}

.modal-table td {
  padding: 12px;
  font-size: 14px;
  color: #262626;
  border-bottom: 1px solid #f0f0f0;
  border-right: 1px solid #f0f0f0;
  text-align: center;
}

.modal-table td:last-child {
  border-right: none;
}

.modal-table tr:last-child td {
  border-bottom: none;
}

.clickable-row {
  cursor: pointer;
}

.clickable-row:hover {
  background-color: #f5f7fa;
}

/* 弹窗内分页 */
.modal-pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
}

.pagination-info {
  font-size: 13px;
  color: #595959;
}

.pagination {
  display: flex;
  gap: 8px;
}

.page-btn {
  min-width: 32px;
  height: 32px;
  padding: 0 8px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  background-color: #fff;
  cursor: pointer;
  font-size: 14px;
  color: #595959;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.page-btn:hover {
  border-color: #1677ff;
  color: #1677ff;
}

.page-btn.active {
  background-color: #1677ff;
  border-color: #1677ff;
  color: #fff;
}

.page-btn:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.checkbox {
  width: 16px;
  height: 16px;
  cursor: pointer;
}
</style>
