const TaskListView = {
  name: 'TaskListView',
  template: `
    <div class="task-list-view">
      <user-header 
        :user="user" 
        @settings="onSettings"
      />
      
      <div class="search-bar animate-fade-in">
        <div class="search-input-wrapper">
          <van-icon name="search" size="18" color="#999" />
          <input 
            type="text" 
            v-model="searchKeyword"
            placeholder="请输入任务名称"
            class="search-input"
            @input="onSearch"
          />
          <van-icon 
            v-if="searchKeyword" 
            name="clear" 
            size="16" 
            color="#999" 
            @click="clearSearch"
            class="clear-icon"
          />
        </div>
      </div>
      
      <div class="task-list-content">
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
          />
        </div>
        
        <div v-if="filteredTasks.length === 0 && !loading" class="empty-state">
          <van-icon name="search" size="48" color="#ccc" />
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
    
    const searchKeyword = Vue.ref('');
    const allTasks = Vue.ref([]);
    const loading = Vue.ref(true);

    const typeMap = {
      routine: { text: '常规监测' },
      supplement: { text: '补充鉴定' },
      special: { text: '专项监测' },
      census: { text: '普查任务' },
      check: { text: '质量核查' }
    }

    const statusMap = {
      pending: { text: '待执行' },
      in_progress: { text: '进行中' },
      completed: { text: '已完成' }
    }

    const mapTask = (item) => ({
      id: String(item.ID),
      title: `${item.SSQH}地块${item.TBH}土壤采样任务`,
      taskNo: item.RWBH,
      type: item.RWLX,
      typeLabel: typeMap[item.RWLX]?.text || item.RWLX,
      location: item.SSQH,
      deadline: item.JHKSSJ,
      completedAt: item.WCSJ,
      status: item.ZT === 'draft' ? 'pending' : item.ZT === 'processing' ? 'in_progress' : item.ZT,
      statusLabel: statusMap[item.ZT]?.text || item.ZT
    })
    
    const fetchTasks = async () => {
      try {
        loading.value = true
        // 从URL参数或localStorage获取当前用户ID，如果没有则使用默认值
        const urlParams = new URLSearchParams(window.location.search);
        const userId = urlParams.get('userId') || localStorage.getItem('currentUserId') || '1';
        const res = await TRJC.api.getTaskList({ page: 1, size: 100, ryid: parseInt(userId) })
        if (res.data.code === 200) {
          allTasks.value = (res.data.data.list || []).map(mapTask)
        }
      } catch (error) {
        console.error('获取任务列表失败:', error)
      } finally {
        loading.value = false
      }
    }

    const filteredTasks = Vue.computed(() => {
      if (!searchKeyword.value) return allTasks.value
      const keyword = searchKeyword.value.toLowerCase()
      return allTasks.value.filter(task => 
        task.title.toLowerCase().includes(keyword) ||
        task.taskNo.toLowerCase().includes(keyword) ||
        task.location.toLowerCase().includes(keyword)
      )
    })
    
    const onSettings = () => {
      vant.showToast('打开设置')
    }
    
    const onSearch = () => {}
    
    const clearSearch = () => {
      searchKeyword.value = ''
    }
    
    const onTaskClick = (task) => {
      vant.showToast(`查看任务: ${task.title}`)
    }

    Vue.onMounted(() => {
      fetchTasks()
    })
    
    return {
      user,
      searchKeyword,
      filteredTasks,
      loading,
      onSettings,
      onSearch,
      clearSearch,
      onTaskClick
    }
  }
}

const TaskListViewStyle = `
.task-list-view {
  min-height: 100vh;
  background-color: var(--bg-color);
  padding-bottom: 20px;
}

.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
}

/* 搜索框样式 */
.search-bar {
  padding: 12px 16px;
  background: var(--card-bg);
  margin: 12px 16px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}

.search-input-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #F5F5F5;
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  transition: all 0.3s ease;
}

.search-input-wrapper:focus-within {
  background: #EEEEEE;
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 14px;
  color: var(--text-primary);
  outline: none;
}

.search-input::placeholder {
  color: var(--text-tertiary);
}

.clear-icon {
  cursor: pointer;
  padding: 2px;
}

/* 任务列表内容 */
.task-list-content {
  margin: 0 16px;
}

.task-list {
  display: flex;
  flex-direction: column;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: var(--text-tertiary);
}

.empty-state p {
  margin-top: 12px;
  font-size: 14px;
}
`;

export { TaskListView, TaskListViewStyle };
