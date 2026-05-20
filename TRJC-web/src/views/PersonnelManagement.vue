<template>
  <div>
    <div class="filter-section">
      <div class="filter-row">
        <div class="filter-item">
          <label class="filter-label">姓名</label>
          <input type="text" class="form-input" placeholder="请输入姓名" v-model="filterForm.keyword">
        </div>
        <div class="filter-item">
          <label class="filter-label">岗位</label>
          <select class="form-select" v-model="filterForm.gw">
            <option value="">全部岗位</option>
            <option value="项目经理">项目经理</option>
            <option value="技术员">技术员</option>
            <option value="采样员">采样员</option>
            <option value="分析员">分析员</option>
          </select>
        </div>
        <div class="filter-item">
          <label class="filter-label">所属区划</label>
          <select class="form-select" v-model="filterForm.ssqh">
            <option value="">全部区划</option>
            <option value="东城区">东城区</option>
            <option value="西城区">西城区</option>
            <option value="朝阳区">朝阳区</option>
            <option value="海淀区">海淀区</option>
            <option value="丰台区">丰台区</option>
          </select>
        </div>
        <div class="filter-item">
          <label class="filter-label">人员状态</label>
          <select class="form-select" v-model="filterForm.ryzt">
            <option value="">全部状态</option>
            <option value="active">在职</option>
            <option value="inactive">离职</option>
          </select>
        </div>
      </div>
      <div class="filter-row">
        <div class="filter-actions">
          <button class="btn btn-default" @click="resetFilter">重置</button>
          <button class="btn btn-primary" @click="handleQuery">查询</button>
          <button class="btn btn-primary" @click="handleAdd">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            新增
          </button>
        </div>
      </div>
    </div>

    <div class="list-section">
      <div class="list-header">
        <h3 class="list-title">人员列表</h3>
      </div>

      <table class="data-table">
        <thead>
          <tr>
            <th style="width: 40px;"><input type="checkbox" class="checkbox" v-model="selectAll"></th>
            <th>姓名</th>
            <th>联系方式</th>
            <th>岗位</th>
            <th>所属区划</th>
            <th>所属部门</th>
            <th>人员状态</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="person in personList" :key="person.ID">
            <td><input type="checkbox" class="checkbox" v-model="person.selected"></td>
            <td>
              <div class="person-info">
                <span class="user-avatar" :style="{ background: person.avatarColor }">{{ person.XM ? person.XM.charAt(0) : '' }}</span>
                {{ person.XM }}
              </div>
            </td>
            <td>{{ person.LXFS }}</td>
            <td>{{ person.GW }}</td>
            <td>{{ person.SSQH }}</td>
            <td>{{ person.SSBM }}</td>
            <td>
              <span class="status-tag" :class="getStatusClass(person.RYZT)">
                {{ person.RYZT === 'active' ? '在职' : '离职' }}
              </span>
            </td>
            <td>{{ person.CJSJ ? person.CJSJ.split(' ')[0] : '' }}</td>
            <td>
              <div class="action-links">
                <span class="action-link" @click="handleEdit(person)">编辑</span>
                <span class="action-link" @click="handleDelete(person)">删除</span>
              </div>
            </td>
          </tr>
          <tr v-if="personList.length === 0">
            <td colspan="9" class="empty-cell">暂无数据</td>
          </tr>
        </tbody>
      </table>

      <div class="pagination-wrapper">
        <span class="pagination-info">显示 {{ pagination.start }} 到 {{ pagination.end }} 条，共 {{ pagination.total }} 条记录</span>
        <div class="pagination">
          <button class="page-btn" :disabled="pagination.current === 1" @click="changePage(pagination.current - 1)">&lt;</button>
          <button 
            v-for="page in pagination.pages" 
            :key="page" 
            class="page-btn" 
            :class="{ active: page === pagination.current }"
            @click="changePage(page)"
          >{{ page }}</button>
          <button class="page-btn" :disabled="pagination.current === pagination.totalPages" @click="changePage(pagination.current + 1)">&gt;</button>
        </div>
      </div>
    </div>

    <div v-if="showAddModal" class="modal-overlay" @click.self="closeAddModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="modal-title">新增人员</h3>
          <button class="modal-close" @click="closeAddModal">×</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-item">
              <label class="form-label">姓名<span class="required">*</span></label>
              <input type="text" class="form-input" placeholder="请输入姓名" v-model="addForm.XM">
            </div>
            <div class="form-item">
              <label class="form-label">联系方式<span class="required">*</span></label>
              <input type="text" class="form-input" placeholder="请输入联系方式" v-model="addForm.LXFS">
            </div>
          </div>
          <div class="form-row">
            <div class="form-item">
              <label class="form-label">岗位</label>
              <select class="form-select" v-model="addForm.GW">
                <option value="">请选择岗位</option>
                <option value="项目经理">项目经理</option>
                <option value="技术员">技术员</option>
                <option value="采样员">采样员</option>
                <option value="分析员">分析员</option>
              </select>
            </div>
            <div class="form-item">
              <label class="form-label">所属区划</label>
              <select class="form-select" v-model="addForm.SSQH">
                <option value="">请选择区划</option>
                <option value="东城区">东城区</option>
                <option value="西城区">西城区</option>
                <option value="朝阳区">朝阳区</option>
                <option value="海淀区">海淀区</option>
                <option value="丰台区">丰台区</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-item">
              <label class="form-label">所属部门</label>
              <input type="text" class="form-input" placeholder="请输入所属部门" v-model="addForm.SSBM">
            </div>
            <div class="form-item">
              <label class="form-label">人员状态<span class="required">*</span></label>
              <select class="form-select" v-model="addForm.RYZT">
                <option value="active">在职</option>
                <option value="inactive">离职</option>
              </select>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-default" @click="closeAddModal">取消</button>
          <button class="btn btn-primary" @click="confirmAdd">确定</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { getPersonnelList, createPersonnel, deletePersonnel } from '../api'

const filterForm = reactive({
  keyword: '',
  gw: '',
  ssqh: '',
  ryzt: ''
})

const selectAll = ref(false)
const personList = ref([])

const showAddModal = ref(false)
const addForm = reactive({
  XM: '',
  LXFS: '',
  GW: '',
  SSQH: '',
  SSBM: '',
  RYZT: 'active'
})

const pagination = reactive({
  current: 1,
  total: 0,
  pageSize: 10,
  pages: [],
  get start() { return (this.current - 1) * this.pageSize + 1 },
  get end() { return Math.min(this.current * this.pageSize, this.total) },
  get totalPages() { return Math.ceil(this.total / this.pageSize) }
})

const getStatusClass = (status) => {
  return status === 'active' ? 'status-active' : 'status-inactive'
}

const avatarColors = [
  'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
  'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
  'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
  'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
]

const fetchList = async () => {
  try {
    const params = {
      page: pagination.current,
      size: pagination.pageSize,
      keyword: filterForm.keyword || undefined,
      gw: filterForm.gw || undefined,
      ssqh: filterForm.ssqh || undefined
    }
    const res = await getPersonnelList(params)
    if (res.data.code === 200) {
      personList.value = (res.data.data.list || []).map((item, index) => ({
        ...item,
        selected: false,
        avatarColor: avatarColors[index % avatarColors.length]
      }))
      pagination.total = res.data.data.total || 0
      const totalPages = Math.ceil(pagination.total / pagination.pageSize)
      pagination.pages = Array.from({ length: Math.min(totalPages, 5) }, (_, i) => i + 1)
    }
  } catch (error) {
    console.error('获取人员列表失败:', error)
  }
}

const resetFilter = () => {
  filterForm.keyword = ''
  filterForm.gw = ''
  filterForm.ssqh = ''
  filterForm.ryzt = ''
  pagination.current = 1
  fetchList()
}

const handleQuery = () => {
  pagination.current = 1
  fetchList()
}

const handleAdd = () => {
  showAddModal.value = true
}

const closeAddModal = () => {
  showAddModal.value = false
  addForm.XM = ''
  addForm.LXFS = ''
  addForm.GW = ''
  addForm.SSQH = ''
  addForm.SSBM = ''
  addForm.RYZT = 'active'
}

const confirmAdd = async () => {
  if (!addForm.XM || !addForm.LXFS) {
    alert('请填写必填项')
    return
  }
  try {
    await createPersonnel(addForm)
    alert('添加成功')
    closeAddModal()
    fetchList()
  } catch (error) {
    console.error('添加失败:', error)
    alert('添加失败')
  }
}

const handleEdit = (person) => {
  console.log('编辑', person)
}

const handleDelete = async (person) => {
  if (!confirm(`确定删除人员 ${person.XM} 吗？`)) return
  try {
    await deletePersonnel(person.ID)
    alert('删除成功')
    fetchList()
  } catch (error) {
    console.error('删除失败:', error)
    alert('删除失败')
  }
}

const changePage = (page) => {
  if (page >= 1 && page <= pagination.totalPages) {
    pagination.current = page
    fetchList()
  }
}

onMounted(() => {
  fetchList()
})
</script>

<style scoped>
.filter-section {
  background-color: #fff;
  padding: 24px;
  border-radius: 8px;
  margin-bottom: 24px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}
.filter-row {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}
.filter-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.filter-label {
  font-size: 13px;
  color: #595959;
  font-weight: 500;
}
.filter-actions {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}
.list-section {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}
.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #f0f0f0;
}
.list-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
}
.data-table {
  width: 100%;
  border-collapse: collapse;
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
  padding: 16px;
  font-size: 14px;
  color: #262626;
  border-bottom: 1px solid #f0f0f0;
  border-right: 1px solid #f0f0f0;
  text-align: center;
}
.data-table td:last-child {
  border-right: none;
}
.data-table tr:hover {
  background-color: #fafafa;
}
.person-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.user-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 12px;
}
.status-tag {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
}
.status-active {
  background-color: #f6ffed;
  color: #52c41a;
}
.status-inactive {
  background-color: #f5f5f5;
  color: #8c8c8c;
}
.action-links {
  display: flex;
  gap: 12px;
  justify-content: center;
}
.action-link {
  color: #1677ff;
  cursor: pointer;
  font-size: 14px;
}
.action-link:hover {
  text-decoration: underline;
}
.empty-cell {
  text-align: center;
  color: #8c8c8c;
  padding: 40px;
}
.pagination-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-top: 1px solid #f0f0f0;
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
.form-input {
  width: 160px;
  height: 36px;
  padding: 0 12px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  font-size: 14px;
  color: #262626;
  background-color: #fff;
  transition: all 0.3s;
}
.form-input:hover {
  border-color: #4096ff;
}
.form-input:focus {
  outline: none;
  border-color: #1677ff;
  box-shadow: 0 0 0 2px rgba(22, 119, 255, 0.1);
}
.form-input::placeholder {
  color: #bfbfbf;
}
.form-select {
  width: 160px;
  height: 36px;
  padding: 0 12px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  font-size: 14px;
  color: #262626;
  background-color: #fff;
  cursor: pointer;
  transition: all 0.3s;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%238c8c8c' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 32px;
}
.form-select:hover {
  border-color: #4096ff;
}
.form-select:focus {
  outline: none;
  border-color: #1677ff;
  box-shadow: 0 0 0 2px rgba(22, 119, 255, 0.1);
}
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
  width: 600px;
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
}
.modal-body .form-row {
  display: flex;
  gap: 24px;
  margin-bottom: 20px;
}
.modal-body .form-row:last-child {
  margin-bottom: 0;
}
.modal-body .form-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.modal-body .form-label {
  font-size: 14px;
  color: #262626;
  font-weight: 500;
}
.modal-body .form-label .required {
  color: #f5222d;
  margin-left: 4px;
}
.modal-body .form-input,
.modal-body .form-select {
  width: 100%;
  height: 40px;
}
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid #f0f0f0;
}
</style>
