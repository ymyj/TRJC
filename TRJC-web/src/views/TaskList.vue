<template>
  <div>
    <!-- 筛选区域 -->
    <div class="filter-section">
      <div class="filter-row">
        <div class="filter-item">
          <label class="filter-label">任务状态</label>
          <select class="form-select" v-model="filterForm.status">
            <option value="">全部状态</option>
            <option value="draft">待发布</option>
            <option value="pending">待分配</option>
            <option value="processing">进行中</option>
            <option value="completed">已完成</option>
          </select>
        </div>
        <div class="filter-item">
          <label class="filter-label">任务类型</label>
          <select class="form-select" v-model="filterForm.type">
            <option value="">全部类型</option>
            <option value="routine">常规监测</option>
            <option value="supplement">补充鉴定</option>
            <option value="special">专项监测</option>
            <option value="census">普查任务</option>
            <option value="check">质量核查</option>
          </select>
        </div>
        <div class="filter-item">
          <label class="filter-label">所属区划</label>
          <select class="form-select" v-model="filterForm.area">
            <option value="">全部区划</option>
            <option value="dongcheng">东城区</option>
            <option value="xicheng">西城区</option>
            <option value="chaoyang">朝阳区</option>
            <option value="haidian">海淀区</option>
            <option value="fengtai">丰台区</option>
          </select>
        </div>
        <div class="filter-item">
          <label class="filter-label">负责人</label>
          <input type="text" class="form-input" placeholder="请输入负责人" v-model="filterForm.person">
        </div>
        <div class="filter-item">
          <label class="filter-label">创建时间</label>
          <input type="text" class="form-input" placeholder="请选择时间范围" v-model="filterForm.time">
        </div>
      </div>
      <div class="filter-row">
        <div class="filter-actions">
          <button class="btn btn-default" @click="resetFilter">重置</button>
          <button class="btn btn-primary" @click="handleQuery">查询</button>
          <button class="btn btn-primary" @click="goToPublish">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            新建
          </button>
        </div>
      </div>
    </div>

    <!-- 列表区域 -->
    <div class="list-section">
      <div class="list-header">
        <h3 class="list-title">任务列表</h3>
      </div>

      <table class="data-table">
        <thead>
          <tr>
            <th style="width: 40px;"><input type="checkbox" class="checkbox" v-model="selectAll"></th>
            <th>任务名称</th>
            <th>任务类型</th>
            <th>所属区划</th>
            <th>负责人</th>
            <th>状态</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="task in taskList" :key="task.RWBH">
            <td><input type="checkbox" class="checkbox" v-model="task.selected"></td>
            <td>
              <div class="task-info">
                <span class="task-name">{{ task.RWBH }} - {{ task.RWMC }}</span>
                <span class="task-desc">{{ task.description }}</span>
              </div>
            </td>
            <td>
              <span class="tag" :class="getTypeClass(task.RWLX)">{{ getTypeText(task.RWLX) }}</span>
            </td>
            <td>{{ task.SSQH }}</td>
            <td>
              <span class="user-avatar" :style="{ background: getAvatarColor(task.FZR) }">{{ task.FZR.charAt(0) }}</span>
              {{ task.FZR }}
            </td>
            <td>
              <span class="status-tag" :class="getStatusClass(task.ZT)">
                <span class="status-dot"></span>
                {{ getStatusText(task.ZT) }}
              </span>
            </td>
            <td>{{ task.CJSJ }}</td>
            <td>
              <div class="action-links">
                <span class="action-link" @click="viewDetail(task)">详情</span>
                <template v-for="(action, index) in getActionButtons(task.ZT)" :key="action.key">
                  <span class="action-link" @click="handleAction(task, action.key)">{{ action.label }}</span>
                </template>
              </div>
            </td>
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
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getTaskList, getTaskStats, publishTask, deleteTask, updateTask } from '../api'

const router = useRouter()

const filterForm = reactive({
  status: '',
  type: '',
  area: '',
  person: '',
  time: ''
})

const viewMode = ref('list')
const selectAll = ref(false)
const taskList = ref([])

const pagination = reactive({
  current: 1,
  total: 0,
  pageSize: 10,
  pages: [],
  get start() { return (this.current - 1) * this.pageSize + 1 },
  get end() { return Math.min(this.current * this.pageSize, this.total) },
  get totalPages() { return Math.ceil(this.total / this.pageSize) }
})

const typeMap = {
  routine: { text: '常规监测', class: 'tag-blue' },
  supplement: { text: '补充鉴定', class: 'tag-purple' },
  special: { text: '专项监测', class: 'tag-red' },
  census: { text: '普查任务', class: 'tag-cyan' },
  check: { text: '质量核查', class: 'tag-orange' }
}

const statusMap = {
  draft: { text: '待发布', class: 'status-default' },
  pending: { text: '待分配', class: 'status-pending' },
  processing: { text: '进行中', class: 'status-processing' },
  completed: { text: '已完成', class: 'status-completed' }
}

const avatarColors = [
  'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
  'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
  'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
  'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
]

const getTypeClass = (type) => {
  return typeMap[type]?.class || 'tag-blue'
}

const getTypeText = (type) => {
  return typeMap[type]?.text || type
}

const getStatusClass = (status) => {
  return statusMap[status]?.class || 'status-default'
}

const getStatusText = (status) => {
  return statusMap[status]?.text || status
}

const getAvatarColor = (name) => {
  let hash = 0
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash)
  }
  return avatarColors[Math.abs(hash) % avatarColors.length]
}

const getActionButtons = (status) => {
  const map = {
    draft: [
      { key: 'edit', label: '编辑' },
      { key: 'delete', label: '删除' },
      { key: 'publish', label: '发布' }
    ],
    pending: [
      { key: 'assign', label: '分配' }
    ],
    processing: [],
    completed: []
  }
  return map[status] || []
}

const fetchList = async () => {
  const params = {
    page: pagination.current,
    size: pagination.pageSize
  }
  if (filterForm.status) params.zt = filterForm.status
  if (filterForm.area) params.ssqh = filterForm.area
  if (filterForm.person) params.keyword = filterForm.person

  const res = await getTaskList(params)
  if (res.data.code === 200) {
    taskList.value = res.data.data.list || []
    pagination.total = res.data.data.total || 0
    updatePaginationPages()
  }
}

const fetchStats = async () => {
  const res = await getTaskStats()
  if (res.data.code === 200) {
    console.log('任务统计:', res.data.data)
  }
}

const updatePaginationPages = () => {
  const totalPages = pagination.totalPages
  const pages = []
  for (let i = 1; i <= totalPages; i++) {
    if (i === 1 || i === totalPages || Math.abs(i - pagination.current) <= 2) {
      pages.push(i)
    }
  }
  pagination.pages = pages
}

const resetFilter = () => {
  filterForm.status = ''
  filterForm.type = ''
  filterForm.area = ''
  filterForm.person = ''
  filterForm.time = ''
  fetchList()
}

const handleQuery = () => {
  pagination.current = 1
  fetchList()
}

const goToPublish = () => {
  router.push('/tasks/publish')
}

const viewDetail = (task) => {
  router.push(`/tasks/detail/${task.ID}`)
}

const handleAction = async (task, action) => {
  if (action === 'assign') {
    router.push(`/tasks/assign/${task.ID}`)
  } else if (action === 'publish') {
    try {
      const res = await publishTask(task.ID)
      if (res.data.code === 200) {
        task.ZT = 'pending'
        fetchList()
      }
    } catch (error) {
      console.error('发布任务失败:', error)
    }
  } else if (action === 'edit') {
    router.push(`/tasks/publish?editId=${task.ID}`)
  } else if (action === 'delete') {
    try {
      const res = await deleteTask(task.ID)
      if (res.data.code === 200) {
        fetchList()
      }
    } catch (error) {
      console.error('删除任务失败:', error)
    }
  }
}

const refresh = () => {
  fetchList()
}

const changePage = (page) => {
  if (page >= 1 && page <= pagination.totalPages) {
    pagination.current = page
    fetchList()
  }
}

onMounted(() => {
  fetchList()
  fetchStats()
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

.list-actions {
  display: flex;
  gap: 8px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  background-color: #fafafa;
  padding: 12px 16px;
  text-align: left;
  font-size: 13px;
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

.task-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.task-name {
  font-weight: 500;
  color: #262626;
}

.task-desc {
  font-size: 12px;
  color: #8c8c8c;
}

.action-links {
  display: flex;
  gap: 12px;
}

.action-link {
  color: #1677ff;
  cursor: pointer;
  font-size: 14px;
}

.action-link:hover {
  text-decoration: underline;
}

.action-more {
  color: #8c8c8c;
  cursor: pointer;
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

/* 待发布状态样式 */
.status-default {
  background-color: #f5f5f5;
  color: #595959;
}

.status-default .status-dot {
  background-color: #8c8c8c;
}
</style>
