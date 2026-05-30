const HomeView = {
  name: 'HomeView',
  components: {
    UserHeader: UserHeader,
    TaskStats: TaskStats,
    TaskItem: TaskItem
  },
  template: `
    <div class="home-view">
      <user-header 
        :user="user" 
        @settings="onSettings"
      />
      
      <div class="welcome-banner animate-fade-in">
        <div class="welcome-greeting">
          <span class="greeting-text">你好，{{ user.name }}</span>
          <span class="greeting-sub">欢迎回来，今天也要加油哦！</span>
        </div>
        <div class="welcome-icon">
          <van-icon name="smile-o" size="40" color="#4A90E2" />
        </div>
      </div>
      
      <task-stats 
        :stats="taskStats" 
        @click="onStatClick"
      />
      
      <div class="task-list-section">
        <div class="section-label">
          <span class="label-bar"></span>
          <span class="label-text">最近任务</span>
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
        
        <div class="view-all-btn" @click="viewAllTasks">
          <span>查看全部任务</span>
          <van-icon name="arrow" size="16" />
        </div>
      </div>
    </div>
  `,
  setup() {
    const router = VueRouter.useRouter()
    
    const user = Vue.ref({
      id: '',
      name: '',
      avatar: '',
      role: '',
      district: ''
    })

    const taskStats = Vue.ref({
      inProgress: 0,
      completed: 0
    })

    const recentTasks = Vue.ref([])

    const typeLabelMap = {
      'routine': '常规监测',
      'supplement': '补充鉴定',
      'special': '专项监测',
      'census': '普查任务',
      'check': '质量核查'
    }

    const statusLabelMap = {
      'draft': '待发布',
      'pending': '待采样',
      'processing': '采样中',
      'completed': '已完成'
    }

    const mapTask = (item) => ({
      id: item.ID,
      title: item.RWMC,
      taskNo: item.RWBH,
      type: item.RWLX,
      typeLabel: typeLabelMap[item.RWLX] || item.RWLX,
      leader: item.FZR || '',
      location: item.SSQH,
      deadline: item.CJSJ ? item.CJSJ.split(' ')[0] : '',
      status: item.ZT === 'draft' ? 'pending' : item.ZT === 'processing' ? 'in_progress' : item.ZT,
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
        const res = await TRJC.api.getTaskList(params)
        if (res.data.code === 200) {
          recentTasks.value = (res.data.data.list || []).map(item => mapTask(item))
        }
      } catch (error) {
        console.error('获取任务列表失败:', error)
      }
    }

    const fetchTaskStats = async () => {
      try {
        const res = await TRJC.api.getTaskStats()
        if (res.data.code === 200) {
          taskStats.value = {
            inProgress: res.data.data.inProgress || 0,
            completed: res.data.data.completed || 0
          }
        }
      } catch (error) {
        console.error('获取任务统计失败:', error)
      }
    }

    const onSettings = async () => {
      if (!confirm('确定要退出登录吗？')) return
      try {
        await TRJC.api.logout()
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

    Vue.onMounted(() => {
      loadUserInfo()
      fetchTaskList()
      fetchTaskStats()
    })
    
    return {
      user,
      taskStats,
      recentTasks,
      onSettings,
      onStatClick,
      onTaskClick,
      viewAllTasks
    }
  }
}

const HomeViewStyle = `
.home-view {
  min-height: 100vh;
  background-color: #F5F8FF;
  padding-bottom: 20px;
}

.welcome-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 0 16px 16px;
  padding: 20px;
  background: linear-gradient(135deg, #E3F2FD 0%, #F5F8FF 100%);
  border-radius: 16px;
}

.welcome-greeting {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.greeting-text {
  font-size: 20px;
  font-weight: 700;
  color: #1A1A1A;
}

.greeting-sub {
  font-size: 13px;
  color: #999;
}

.task-list-section {
  margin: 0 16px;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.label-bar {
  width: 4px;
  height: 18px;
  border-radius: 2px;
  background: #4A90E2;
}

.label-text {
  font-size: 17px;
  font-weight: 700;
  color: #1A1A1A;
}

.task-list {
  display: flex;
  flex-direction: column;
}

.view-all-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 14px;
  margin-top: 16px;
  background: #fff;
  border-radius: 12px;
  font-size: 14px;
  color: #4A90E2;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.2s ease;
}

.view-all-btn:active {
  background: #F0F4FF;
}
`;

export { HomeView, HomeViewStyle };