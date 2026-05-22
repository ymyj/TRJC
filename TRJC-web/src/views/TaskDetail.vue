<template>
  <div>
    <div class="page-header">
      <button class="btn-back" @click="goBack">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
        返回
      </button>
      <h1 class="page-title">任务详情</h1>
    </div>

    <div class="detail-card">
      <!-- 标签页 -->
      <div class="tabs">
        <div 
          class="tab-item" 
          :class="{ active: activeTab === 'basic' }"
          @click="activeTab = 'basic'"
        >
          基本信息
        </div>
        <div 
          class="tab-item" 
          :class="{ active: activeTab === 'land' }"
          @click="activeTab = 'land'"
        >
          采样地块
        </div>
      </div>

      <!-- 基本信息 -->
      <div v-if="activeTab === 'basic'" class="tab-content">
        <div class="info-grid">
          <div class="info-item">
            <label class="info-label">任务编号</label>
            <span class="info-value">{{ taskInfo.code }}</span>
          </div>
          <div class="info-item">
            <label class="info-label">项目负责人</label>
            <div class="info-value">
              <span class="user-avatar" :style="{ background: taskInfo.personAvatar }">{{ taskInfo.person?.charAt(0) }}</span>
              {{ taskInfo.person }}
            </div>
          </div>
          <div class="info-item">
            <label class="info-label">计划开始时间</label>
            <span class="info-value">{{ taskInfo.planStartTime }}</span>
          </div>
          <div class="info-item">
            <label class="info-label">任务名称</label>
            <span class="info-value">{{ taskInfo.name }}</span>
          </div>
          <div class="info-item">
            <label class="info-label">联系电话</label>
            <span class="info-value">{{ taskInfo.contact }}</span>
          </div>
          <div class="info-item">
            <label class="info-label">实际开始时间</label>
            <span class="info-value">{{ taskInfo.actualStartTime }}</span>
          </div>
          <div class="info-item">
            <label class="info-label">所属区域</label>
            <span class="info-value">{{ taskInfo.area }}</span>
          </div>
          <div class="info-item">
            <label class="info-label">任务类型</label>
            <span class="info-value">{{ getTypeText(taskInfo.type) }}</span>
          </div>
        </div>

        <div class="desc-section">
          <h4 class="desc-title">任务描述</h4>
          <div class="desc-content">
            <p>{{ taskInfo.description }}</p>
            <p>{{ taskInfo.requirement }}</p>
            <p>{{ taskInfo.notice }}</p>
          </div>
        </div>
      </div>

      <!-- 采样地块 -->
      <div v-if="activeTab === 'land'" class="tab-content">
        <table class="data-table">
          <thead>
            <tr>
              <th>图斑编号</th>
              <th>所属单元</th>
              <th>图斑面积（㎡）</th>
              <th>所属区划</th>
              <th>经度</th>
              <th>纬度</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="land in landList" :key="land.id">
              <td>{{ land.code }}</td>
              <td>{{ land.unit }}</td>
              <td>{{ land.area }}</td>
              <td>{{ land.district }}</td>
              <td>{{ land.longitude }}</td>
              <td>{{ land.latitude }}</td>
              <td>
                <span class="status-tag" :class="getLandStatusClass(land.status)">
                  {{ land.statusText }}
                </span>
              </td>
              <td>
                <span class="action-link" @click="viewLandDetail(land)">详情</span>
              </td>
            </tr>
            <tr v-if="landList.length === 0">
              <td colspan="8" class="empty-cell">暂无数据</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getTaskDetail } from '../api'

const router = useRouter()
const route = useRoute()
const activeTab = ref('basic')
const taskInfo = reactive({
  code: '',
  name: '',
  area: '',
  type: '',
  person: '',
  personAvatar: '',
  contact: '',
  planStartTime: '',
  actualStartTime: '',
  description: '',
  requirement: '',
  notice: '',
  createTime: '',
  status: ''
})

const typeMap = {
  routine: '常规监测',
  supplement: '补充鉴定',
  special: '专项监测',
  census: '普查任务',
  check: '质量核查'
}

const statusMap = {
  pending: { text: '待分配', class: 'status-pending' },
  processing: { text: '进行中', class: 'status-processing' },
  completed: { text: '已完成', class: 'status-completed' }
}

const getTypeText = (type) => {
  return typeMap[type] || type
}

const getStatusClass = (status) => {
  return statusMap[status]?.class || 'status-pending'
}

const getStatusText = (status) => {
  return statusMap[status]?.text || status
}
const landList = ref([])

const avatarColors = [
  'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
  'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
  'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
  'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
]

const landStatusMap = {
  pending: { text: '待领取', class: 'status-pending' },
  sampling: { text: '待采样', class: 'status-sampling' },
  transport: { text: '待运输', class: 'status-transport' },
  analysis: { text: '待分析', class: 'status-analysis' },
  completed: { text: '已完成', class: 'status-completed' }
}

const getLandStatusClass = (status) => {
  return landStatusMap[status]?.class || 'status-pending'
}

const fetchTaskDetail = async () => {
  try {
    const taskId = route.params.id
    const res = await getTaskDetail(taskId)
    if (res.data.code === 200) {
      const data = res.data.data
      Object.assign(taskInfo, {
        code: data.RWBH || '',
        name: data.RWMC || '',
        area: data.SSQH || '',
        type: data.RWLX || '',
        person: data.FZR || '',
        personAvatar: avatarColors[0],
        contact: data.LXDH || '',
        planStartTime: data.JHKSSJ || '',
        actualStartTime: '',
        description: data.RWMS || '',
        requirement: '',
        notice: '',
        createTime: data.CJSJ || '',
        status: data.ZT || ''
      })
      landList.value = (data.plots || []).map(item => ({
        id: item.ID,
        code: item.TBH,
        unit: item.SSDY,
        area: item.TBMJ,
        district: item.SSQH,
        longitude: item.JD,
        latitude: item.WD,
        status: item.status || 'pending',
        statusText: item.statusLabel || '待领取'
      }))
    }
  } catch (error) {
    console.error('获取任务详情失败:', error)
  }
}

const goBack = () => {
  router.push('/tasks')
}

const viewLandDetail = (land) => {
  router.push({ name: 'LandDetail', params: { id: land.id }, query: { taskId: route.params.id } })
}

onMounted(() => {
  fetchTaskDetail()
})
</script>

<style scoped>
.page-header {
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.btn-back {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  background-color: #fff;
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
}

.detail-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

/* 标签页 */
.tabs {
  display: flex;
  border-bottom: 1px solid #f0f0f0;
  background-color: #fafafa;
}

.tab-item {
  padding: 14px 24px;
  font-size: 14px;
  color: #595959;
  cursor: pointer;
  transition: all 0.3s;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
}

.tab-item:hover {
  color: #1677ff;
}

.tab-item.active {
  color: #1677ff;
  background-color: #fff;
  border-bottom-color: #1677ff;
  font-weight: 500;
}

/* 标签内容 */
.tab-content {
  padding: 24px;
}

/* 信息网格 */
.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-label {
  font-size: 13px;
  color: #8c8c8c;
}

.info-value {
  font-size: 14px;
  color: #262626;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 12px;
}

/* 任务描述 */
.desc-section {
  border-top: 1px solid #f0f0f0;
  padding-top: 24px;
}

.desc-title {
  font-size: 14px;
  font-weight: 600;
  color: #262626;
  margin-bottom: 16px;
}

.desc-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.desc-content p {
  font-size: 14px;
  color: #595959;
  line-height: 1.8;
}

/* 表格样式 */
.data-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #f0f0f0;
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

.data-table tr:hover {
  background-color: #fafafa;
}

.empty-cell {
  text-align: center;
  color: #8c8c8c;
  padding: 40px;
}

/* 状态标签 */
.status-tag {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
}

.status-pending {
  background-color: #fff7e6;
  color: #fa8c16;
}

.status-sampling {
  background-color: #e6f7ff;
  color: #1890ff;
}

.status-transport {
  background-color: #f6ffed;
  color: #52c41a;
}

.status-analysis {
  background-color: #f9f0ff;
  color: #722ed1;
}

.status-completed {
  background-color: #f6ffed;
  color: #52c41a;
}

/* 操作链接 */
.action-link {
  color: #1677ff;
  cursor: pointer;
  font-size: 14px;
}

.action-link:hover {
  text-decoration: underline;
}
</style>
