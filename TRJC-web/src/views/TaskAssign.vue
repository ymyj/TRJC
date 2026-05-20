<template>
  <div class="task-assign-page">
    <div class="page-header">
      <button class="btn-back" @click="goBack">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
        返回
      </button>
      <h2 class="page-title">任务分配</h2>
    </div>

    <!-- 任务信息 -->
    <div class="task-info-card" v-if="taskInfo">
      <div class="info-row">
        <div class="info-item">
          <label class="info-label">任务编号</label>
          <span class="info-value">{{ taskInfo.RWBH }}</span>
        </div>
        <div class="info-item">
          <label class="info-label">任务名称</label>
          <span class="info-value">{{ taskInfo.RWMC }}</span>
        </div>
        <div class="info-item">
          <label class="info-label">任务类型</label>
          <span class="info-value">{{ getTypeText(taskInfo.RWLX) }}</span>
        </div>
        <div class="info-item">
          <label class="info-label">所属区划</label>
          <span class="info-value">{{ taskInfo.SSQH }}</span>
        </div>
        <div class="info-item">
          <label class="info-label">负责人</label>
          <span class="info-value">{{ taskInfo.FZR }}</span>
        </div>
        <div class="info-item">
          <label class="info-label">状态</label>
          <span class="status-tag" :class="getStatusClass(taskInfo.ZT)">
            <span class="status-dot"></span>
            {{ getStatusText(taskInfo.ZT) }}
          </span>
        </div>
      </div>
    </div>

    <div class="list-section">
      <table class="data-table">
        <thead>
          <tr>
            <th>图斑编号</th>
            <th>所属单元</th>
            <th>图斑面积（㎡）</th>
            <th>所属区划</th>
            <th>经度</th>
            <th>纬度</th>
            <th>采样人员</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in plotList" :key="item.ID">
            <td>{{ item.TBH }}</td>
            <td>{{ item.SSDY }}</td>
            <td>{{ item.TBMJ }}</td>
            <td>{{ item.SSQH }}</td>
            <td>{{ item.JD }}</td>
            <td>{{ item.WD }}</td>
            <td>{{ getSamplersText(item.ID) }}</td>
            <td>
              <span class="action-link" @click="openPersonSelect(item)">人员分配</span>
            </td>
          </tr>
          <tr v-if="plotList.length === 0">
            <td colspan="8" class="empty-cell">暂无地块数据</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="personModalVisible" class="modal-overlay" @click="closePersonModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3 class="modal-title">人员选择</h3>
          <button class="modal-close" @click="closePersonModal">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div class="filter-section-modal">
          <div class="filter-row-modal">
            <div class="filter-item-modal">
              <label class="filter-label-modal">人员姓名</label>
              <input type="text" class="form-input-modal" placeholder="请输入" v-model="personFilter.name">
            </div>
            <div class="filter-item-modal">
              <label class="filter-label-modal">所属区划</label>
              <select class="form-select-modal" v-model="personFilter.district">
                <option value="">请选择</option>
                <option v-for="district in districtOptions" :key="district" :value="district">{{ district }}</option>
              </select>
            </div>
          </div>
        </div>

        <div class="person-list-section">
          <table class="person-table">
            <thead>
              <tr>
                <th style="width: 40px;">
                  <input type="checkbox" class="checkbox" v-model="selectAll" @change="handleSelectAll">
                </th>
                <th>姓名</th>
                <th>联系方式</th>
                <th>岗位</th>
                <th>所属区划</th>
                <th>所属部门</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="person in filteredPersonList" :key="person.ID" @click="toggleSelect(person)" class="person-row">
                <td @click.stop>
                  <input type="checkbox" class="checkbox" v-model="person.selected" @change="handleSelectChange">
                </td>
                <td>
                  <div class="person-info">
                    <span class="person-avatar" :style="{ background: person.avatarColor }">{{ person.XM?.charAt(0) }}</span>
                    {{ person.XM }}
                  </div>
                </td>
                <td>{{ person.LXFS }}</td>
                <td>{{ person.GW }}</td>
                <td>{{ person.SSQH }}</td>
                <td>{{ person.SSBM }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="modal-footer">
          <button class="btn btn-default" @click="closePersonModal">取消</button>
          <button class="btn btn-primary" @click="confirmAssign">确定</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getTaskDetail, getPersonnelForAssignment, assignTask } from '../api'

const router = useRouter()
const route = useRoute()

const taskId = ref(route.params.id)
const taskInfo = ref(null)
const plotList = ref([])
const allAssignments = ref({})

const personModalVisible = ref(false)
const currentPlot = ref(null)
const personFilter = reactive({
  name: '',
  district: ''
})
const selectAll = ref(false)
const personList = ref([])
const districtOptions = ref([])

const typeMap = {
  routine: '常规监测',
  supplement: '补充鉴定',
  special: '专项监测',
  census: '普查任务',
  check: '质量核查'
}

const statusMap = {
  draft: { text: '草稿', class: 'status-pending' },
  pending: { text: '待分配', class: 'status-pending' },
  processing: { text: '进行中', class: 'status-processing' },
  completed: { text: '已完成', class: 'status-completed' }
}

const getTypeText = (type) => typeMap[type] || type
const getStatusClass = (status) => statusMap[status]?.class || 'status-pending'
const getStatusText = (status) => statusMap[status]?.text || status

const filteredPersonList = computed(() => {
  return personList.value.filter(person => {
    const matchName = !personFilter.name || person.XM?.includes(personFilter.name)
    const matchDistrict = !personFilter.district || person.SSQH === personFilter.district
    return matchName && matchDistrict
  })
})

const getSamplersText = (plotId) => {
  const ids = allAssignments.value[plotId] || []
  if (ids.length === 0) return '-'
  const names = personList.value
    .filter(p => ids.includes(p.ID))
    .map(p => p.XM)
  return names.join('、') || '-'
}

const avatarColors = [
  'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
  'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
  'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
  'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
]

const fetchTaskDetail = async () => {
  const res = await getTaskDetail(taskId.value)
  if (res.data.code === 200) {
    const data = res.data.data
    taskInfo.value = data
    plotList.value = data.plots || []
    allAssignments.value = {}
    if (data.plots && data.assignee_ids) {
      data.plots.forEach(plot => {
        allAssignments.value[plot.ID] = data.assignee_ids
      })
    }
  }
}

const fetchPersonnelList = async () => {
  const res = await getPersonnelForAssignment({ page: 1, size: 100 })
  if (res.data.code === 200) {
    const list = res.data.data.list || []
    personList.value = list.map((item, index) => ({
      ...item,
      avatarColor: avatarColors[index % avatarColors.length],
      selected: false
    }))
    const districts = [...new Set(list.map(p => p.SSQH).filter(Boolean))]
    districtOptions.value = districts
  }
}

const openPersonSelect = (plot) => {
  currentPlot.value = plot
  personModalVisible.value = true
  const assignedIds = allAssignments.value[plot.ID] || []
  personList.value.forEach(person => {
    person.selected = assignedIds.includes(person.ID)
  })
  selectAll.value = filteredPersonList.value.length > 0 &&
    filteredPersonList.value.every(person => person.selected)
}

const closePersonModal = () => {
  personModalVisible.value = false
  currentPlot.value = null
}

const handleSelectAll = () => {
  filteredPersonList.value.forEach(person => {
    person.selected = selectAll.value
  })
}

const handleSelectChange = () => {
  selectAll.value = filteredPersonList.value.length > 0 &&
    filteredPersonList.value.every(person => person.selected)
}

const toggleSelect = (person) => {
  person.selected = !person.selected
  handleSelectChange()
}

const confirmAssign = async () => {
  const selectedPersons = personList.value.filter(person => person.selected)
  if (selectedPersons.length === 0) {
    alert('请选择至少一名人员')
    return
  }

  const personnelIds = selectedPersons.map(p => p.ID)

  try {
    const res = await assignTask(taskId.value, personnelIds)
    if (res.data.code === 200) {
      allAssignments.value[currentPlot.value.ID] = personnelIds
      alert('分配成功')
    }
  } catch (e) {
    alert('分配失败: ' + (e.message || '未知错误'))
    return
  }

  closePersonModal()
}

const goBack = () => {
  router.push('/tasks')
}

onMounted(() => {
  fetchTaskDetail()
  fetchPersonnelList()
})
</script>

<style scoped>
.task-assign-page {
  padding: 24px;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.btn-back {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  background: #fff;
  color: #595959;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-back:hover {
  border-color: #4096ff;
  color: #4096ff;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.list-section {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  background-color: #fafafa;
  padding: 16px;
  text-align: left;
  font-size: 14px;
  font-weight: 500;
  color: #595959;
  border-bottom: 1px solid #f0f0f0;
}

.data-table td {
  padding: 16px;
  font-size: 14px;
  color: #262626;
  border-bottom: 1px solid #f0f0f0;
}

.data-table tr:hover {
  background-color: #fafafa;
}

.action-link {
  color: #1677ff;
  cursor: pointer;
  font-size: 14px;
}

.action-link:hover {
  text-decoration: underline;
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
  background: #fff;
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
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;
}

.modal-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  cursor: pointer;
  color: #8c8c8c;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-close:hover {
  color: #595959;
}

.filter-section-modal {
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;
}

.filter-row-modal {
  display: flex;
  gap: 24px;
}

.filter-item-modal {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-label-modal {
  font-size: 14px;
  color: #595959;
  white-space: nowrap;
}

.form-input-modal,
.form-select-modal {
  width: 160px;
  height: 36px;
  padding: 0 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 14px;
  color: #262626;
  background-color: #fff;
}

.form-select-modal {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%238c8c8c' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 8px center;
  padding-right: 28px;
}

.person-list-section {
  flex: 1;
  overflow: auto;
  padding: 0 24px;
}

.person-table {
  width: 100%;
  border-collapse: collapse;
}

.person-table th {
  background-color: #fafafa;
  padding: 12px 16px;
  text-align: left;
  font-size: 14px;
  font-weight: 500;
  color: #595959;
  border-bottom: 1px solid #f0f0f0;
}

.person-table td {
  padding: 12px 16px;
  font-size: 14px;
  color: #262626;
  border-bottom: 1px solid #f0f0f0;
}

.person-row {
  cursor: pointer;
}

.person-row:hover {
  background-color: #fafafa;
}

.checkbox {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.person-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.person-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid #f0f0f0;
}

.btn {
  height: 36px;
  padding: 0 20px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.btn-default {
  background-color: #fff;
  border: 1px solid #d9d9d9;
  color: #595959;
}

.btn-default:hover {
  border-color: #4096ff;
  color: #4096ff;
}

.btn-primary {
  background-color: #1677ff;
  color: #fff;
}

.btn-primary:hover {
  background-color: #4096ff;
}

.task-info-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  padding: 20px 24px;
  margin-bottom: 24px;
}

.info-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.info-label {
  font-size: 13px;
  color: #8c8c8c;
}

.info-value {
  font-size: 14px;
  color: #262626;
  font-weight: 500;
}

.status-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: currentColor;
}

.status-pending {
  background-color: #fff7e6;
  color: #fa8c16;
}

.status-processing {
  background-color: #e6f7ff;
  color: #1890ff;
}

.status-completed {
  background-color: #f6ffed;
  color: #52c41a;
}

.empty-cell {
  text-align: center;
  color: #8c8c8c;
  padding: 40px;
}
</style>
