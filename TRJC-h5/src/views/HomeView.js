<template>
  <div class="home-view">
    <user-header 
      :user="user" 
      @settings="onSettings"
    />
    
    <task-stats 
      :stats="taskStats" 
      @click="onStatClick"
    />
    
    <div class="task-list-section">
      <div class="section-header">
        <h3 class="section-title">最近任务</h3>
        <span class="view-all" @click="viewAllTasks">查看全部</span>
      </div>
      <div class="task-list">
        <task-item 
          v-for="(task, index) in recentTasks" 
          :key="task.id"
          :task="task"
          :index="index"
          @click="onTaskClick"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getTaskList, getTaskStats, logout } from '../api'
import UserHeader from '../components/UserHeader.js'
import TaskStats from '../components/TaskStats.js'
import TaskItem from '../components/TaskItem.js'

const router = useRouter()

const user = ref({
  id: '',
  name: '',
  avatar: '',
  role: '',
  district: ''
})

const taskStats = ref({
  pending: 0,
  completed: 0,
  toSubmit: 0
})

const recentTasks = ref([])

const typeLabelMap = {
  'routine': '常规监测',
  'supplement': '补充鉴定',
  'special': '专项监测',
  'census': '普查任务',
  'check': '质量核查'
}

const statusLabelMap = {
  'draft': '待发布',
  'pending': '待领取',
  'processing': '进行中',
  'completed': '已完成'
}

const mapTask = (item) => ({
  id: item.ID,
  title: item.RWMC,
  taskNo: item.RWBH,
  type: item.RWLX,
  typeLabel: typeLabelMap[item.RWLX] || item.RWLX,
  location: item.SSQH,
  deadline: item.CJSJ ? item.CJSJ.split(' ')[0] : '',
  status: item.ZT,
  statusLabel: statusLabelMap[item.ZT] || item.ZT
})

const loadUserInfo = () => {
  const info = localStorage.getItem('userInfo')
  if (info) {
    try {
      const parsed = JSON.parse(info)
      user.value = {
        id: parsed.ID || '',
        name: parsed.XM || '',
        avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${parsed.XM}&backgroundColor=b6e3f4`,
        role: parsed.GW || '',
        district: parsed.SSQH || ''
      }
    } catch (e) {
      console.error('解析用户信息失败', e)
    }
  }
}

const fetchTaskList = async () => {
  try {
    const userId = localStorage.getItem('currentUserId')
    if (!userId) return
    const params = { page: 1, size: 10, ryid: parseInt(userId) }
    const res = await getTaskList(params)
    if (res.data.code === 200) {
      recentTasks.value = (res.data.data.list || []).map(item => mapTask(item))
    }
  } catch (error) {
    console.error('获取任务列表失败:', error)
  }
}

const fetchTaskStats = async () => {
  try {
    const res = await getTaskStats()
    if (res.data.code === 200) {
      taskStats.value = {
        pending: res.data.data.pending || 0,
        completed: res.data.data.completed || 0,
        toSubmit: 0
      }
    }
  } catch (error) {
    console.error('获取任务统计失败:', error)
  }
}

const onSettings = async () => {
  if (!confirm('确定要退出登录吗？')) return
  try {
    await logout()
  } catch (error) {
    console.error('退出登录请求失败:', error)
  } finally {
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
    localStorage.removeItem('currentUserId')
    router.push('/login')
  }
}

const onStatClick = (type) => {
  const typeMap = {
    'pending': '待执行任务',
    'completed': '已完成任务',
    'toSubmit': '待提交数据'
  }
  vant.showToast(`查看${typeMap[type]}`)
}

const onTaskClick = (task) => {
  vant.showToast(`查看任务: ${task.title}`)
}

const viewAllTasks = () => {
  router.push('/tasks')
}

onMounted(() => {
  loadUserInfo()
  fetchTaskList()
  fetchTaskStats()
})
</script>

<style scoped>
.home-view {
  min-height: 100vh;
  background-color: var(--bg-color);
  padding-bottom: 20px;
}

.task-list-section {
  margin: 0 16px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-top: 8px;
}

.section-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
}

.view-all {
  font-size: 14px;
  color: var(--primary-color);
  cursor: pointer;
}

.task-list {
  display: flex;
  flex-direction: column;
}
</style>

export { HomeView, HomeViewStyle };
