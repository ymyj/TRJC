const TaskListView = {
  name: 'TaskListView',
  template: `
    <div class="task-list-view">
      <div class="top-nav animate-fade-in">
        <div class="nav-left">
          <van-icon name="wap-nav" size="22" color="#333" />
        </div>
        <span class="nav-title">现场采样任务</span>
        <div class="nav-right">
          <div class="avatar-small">{{ userInitial }}</div>
        </div>
      </div>
      
      <div class="search-bar animate-fade-in">
        <van-icon name="search" size="18" color="#BBB" />
        <input 
          type="text" 
          v-model="searchKeyword"
          placeholder="搜索任务名称、编号或受检单位"
          class="search-input"
          @input="onSearch"
        />
        <van-icon 
          v-if="searchKeyword" 
          name="clear" 
          size="16" 
          color="#BBB" 
          @click="clearSearch"
        />
      </div>
      
      <div class="stats-section">
        <div class="section-label">
          <span class="label-bar"></span>
          <span class="label-text">任务统计</span>
        </div>
        <div class="stats-grid">
          <div class="stat-card stat-card-all" @click="filterByStatus('all')">
            <div class="stat-icon-wrapper">
              <van-icon name="notes-o" size="20" color="#4A90E2" />
            </div>
            <div class="stat-content">
              <span class="stat-title">全部任务</span>
              <span class="stat-value">{{ filteredTasks.length }}</span>
              <span class="stat-subtitle">当前搜索结果</span>
            </div>
          </div>
          <div class="stat-card stat-card-pending" @click="filterByStatus('pending')">
            <div class="stat-icon-wrapper">
              <van-icon name="clock-o" size="20" color="#FF9500" />
            </div>
            <div class="stat-content">
              <span class="stat-title">待采样</span>
              <span class="stat-value">{{ pendingCount }}</span>
              <span class="stat-subtitle">临期 {{ urgentCount }} / 到期 {{ overdueCount }}</span>
            </div>
          </div>
          <div class="stat-card stat-card-inprogress" @click="filterByStatus('in_progress')">
            <div class="stat-icon-wrapper">
              <van-icon name="replay" size="20" color="#4A90E2" />
            </div>
            <div class="stat-content">
              <span class="stat-title">进行中</span>
              <span class="stat-value">{{ inProgressCount }}</span>
              <span class="stat-subtitle">正在执行中</span>
            </div>
          </div>
          <div class="stat-card stat-card-completed" @click="filterByStatus('completed')">
            <div class="stat-icon-wrapper">
              <van-icon name="checked" size="20" color="#34C759" />
            </div>
            <div class="stat-content">
              <span class="stat-title">已完成</span>
              <span class="stat-value">{{ completedCount }}</span>
              <span class="stat-subtitle">完成率 {{ completionRate }}%</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="task-list-section">
        <div class="section-label">
          <span class="label-bar"></span>
          <span class="label-text">任务列表</span>
        </div>
        <div v-if="loading" class="loading-state">
          <van-loading size="24px">加载中...</van-loading>
        </div>
        <div v-else class="task-list">
          <task-item 
            v-for="(task, index) in filteredTasks" 
            :key="task.id"
            :task="task"
            :index="index"
            @click="onTaskClick"
            @detail="onTaskDetail"
            @continue="onContinueSample"
          />
        </div>
        
        <div v-if="filteredTasks.length === 0 && !loading" class="empty-state">
          <van-icon name="search" size="48" color="#DDD" />
          <p>未找到相关任务</p>
        </div>
      </div>
    </div>
  `,
  setup() {
    const user = Vue.ref({
      id: '1',
      name: '张调查员',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=inspector&backgroundColor=b6e3f4',
      role: '外业调查员',
      district: '东城区'
    });
    
    const userInitial = Vue.computed(() => {
      return user.value.name ? user.value.name.charAt(user.value.name.length - 1) : 'U';
    });
    
    const searchKeyword = Vue.ref('');
    const allTasks = Vue.ref([]);
    const loading = Vue.ref(true);
    const currentFilter = Vue.ref('all');

    const typeMap = {
      routine: { text: '常规监测' },
      supplement: { text: '补充鉴定' },
      special: { text: '专项监测' },
      census: { text: '普查任务' },
      check: { text: '质量核查' }
    }

    const statusMap = {
      pending: { text: '待采样' },
      in_progress: { text: '采样中' },
      completed: { text: '已完成' }
    }

    const mapTask = (item) => ({
      id: String(item.ID),
      title: item.SSQH && item.TBH ? `${item.SSQH}地块${item.TBH}土壤采样任务` : `${item.SSQH || ''}采样任务`,
      taskNo: item.RWBH,
      type: item.RWLX,
      typeLabel: typeMap[item.RWLX]?.text || item.RWLX,
      leader: item.FZR || '',
      location: item.SSQH,
      deadline: item.JHKSSJ,
      completedAt: item.WCSJ,
      status: item.ZT === 'draft' ? 'pending' : item.ZT === 'processing' ? 'in_progress' : item.ZT,
      statusLabel: statusMap[item.ZT]?.text || item.ZT,
      personnel: item.CYRY || ''
    })
    
    const fetchTasks = async () => {
      try {
        loading.value = true
        const res = await TRJC.api.getTaskList({ page: 1, size: 100 })
        if (res.data.code === 200) {
          allTasks.value = (res.data.data.list || []).map(mapTask)
        }
      } catch (error) {
        console.error('获取任务列表失败:', error)
      } finally {
        loading.value = false
      }
    }

    const filteredByStatus = Vue.computed(() => {
      if (currentFilter.value === 'all') return allTasks.value;
      return allTasks.value.filter(task => task.status === currentFilter.value);
    });

    const filteredTasks = Vue.computed(() => {
      const tasks = filteredByStatus.value;
      if (!searchKeyword.value) return tasks;
      const keyword = searchKeyword.value.toLowerCase()
      return tasks.filter(task => 
        task.title.toLowerCase().includes(keyword) ||
        task.taskNo.toLowerCase().includes(keyword) ||
        task.location.toLowerCase().includes(keyword)
      )
    });

    const pendingCount = Vue.computed(() => {
      return allTasks.value.filter(t => t.status === 'pending').length;
    });

    const inProgressCount = Vue.computed(() => {
      return allTasks.value.filter(t => t.status === 'in_progress').length;
    });

    const completedCount = Vue.computed(() => {
      return allTasks.value.filter(t => t.status === 'completed').length;
    });

    const urgentCount = Vue.computed(() => {
      const today = new Date();
      return allTasks.value.filter(t => {
        if (t.status !== 'pending' || !t.deadline) return false;
        const diff = Math.ceil((new Date(t.deadline) - today) / (1000 * 60 * 60 * 24));
        return diff >= 0 && diff <= 3;
      }).length;
    });

    const overdueCount = Vue.computed(() => {
      const today = new Date();
      return allTasks.value.filter(t => {
        if (t.status !== 'pending' || !t.deadline) return false;
        return new Date(t.deadline) < today;
      }).length;
    });

    const completionRate = Vue.computed(() => {
      if (allTasks.value.length === 0) return '0';
      return Math.round((completedCount.value / allTasks.value.length) * 100);
    });
    
    const filterByStatus = (status) => {
      currentFilter.value = status;
    };
    
    const onTaskClick = (task) => {
      vant.showToast(`查看任务: ${task.title}`)
    }

    const onTaskDetail = (task) => {
      vant.showToast(`任务详情: ${task.title}`)
    }

    const onContinueSample = (task) => {
      vant.showToast(`继续采样: ${task.title}`)
    }
    
    const onSettings = () => {
      vant.showToast('打开设置')
    }
    
    const onSearch = () => {}
    
    const clearSearch = () => {
      searchKeyword.value = ''
    }

    Vue.onMounted(() => {
      fetchTasks()
    })
    
    return {
      user,
      userInitial,
      searchKeyword,
      filteredTasks,
      filteredByStatus,
      loading,
      currentFilter,
      pendingCount,
      inProgressCount,
      completedCount,
      urgentCount,
      overdueCount,
      completionRate,
      filterByStatus,
      onSettings,
      onSearch,
      clearSearch,
      onTaskClick,
      onTaskDetail,
      onContinueSample
    }
  }
}

const TaskListViewStyle = `
.task-list-view {
  min-height: 100vh;
  background-color: #F5F8FF;
  padding-bottom: 20px;
}

.top-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: #F5F8FF;
}

.nav-left {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-title {
  font-size: 20px;
  font-weight: 700;
  color: #1A1A1A;
}

.nav-right {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-small {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4A90E2 0%, #5BA3F5 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #fff;
  border-radius: 12px;
  padding: 12px 16px;
  margin: 0 16px 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.search-bar .search-input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 14px;
  color: #333;
  outline: none;
}

.search-bar .search-input::placeholder {
  color: #BBB;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 16px 12px;
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

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin: 0 16px 20px;
}

.stat-card {
  background: #fff;
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  display: flex;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.stat-card:active {
  transform: scale(0.98);
}

.stat-icon-wrapper {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-card-all .stat-icon-wrapper {
  background: #E3F2FD;
}

.stat-card-pending .stat-icon-wrapper {
  background: #FFF3E0;
}

.stat-card-inprogress .stat-icon-wrapper {
  background: #E3F2FD;
}

.stat-card-completed .stat-icon-wrapper {
  background: #E8F5E9;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.stat-title {
  font-size: 13px;
  color: #999;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1A1A1A;
  line-height: 1.1;
}

.stat-subtitle {
  font-size: 11px;
  color: #999;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.task-list-section {
  margin: 0 16px;
}

.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
}

.task-list {
  display: flex;
  flex-direction: column;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #BBB;
}

.empty-state p {
  margin-top: 12px;
  font-size: 14px;
}
`;

export { TaskListView, TaskListViewStyle };