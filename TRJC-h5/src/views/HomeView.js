const HomeView = {
  name: 'HomeView',
  template: `
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
  `,
  setup() {
    const user = Vue.ref({
      id: '1',
      name: '张调查员',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=inspector&backgroundColor=b6e3f4',
      role: '外业调查员',
      district: '东城区'
    });

    const taskStats = Vue.ref({
      pending: 0,
      completed: 0,
      toSubmit: 0
    });

    const recentTasks = Vue.ref([]);

    const typeLabelMap = {
      'routine': '常规监测',
      'supplement': '补充鉴定',
      'special': '专项监测',
      'census': '普查任务',
      'check': '质量核查'
    };

    const statusLabelMap = {
      'draft': '待发布',
      'pending': '待领取',
      'processing': '进行中',
      'completed': '已完成'
    };

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
    });

    const fetchTaskList = async () => {
      try {
        // 从URL参数或localStorage获取当前用户ID，如果没有则使用默认值
        const urlParams = new URLSearchParams(window.location.search);
        const userId = urlParams.get('userId') || localStorage.getItem('currentUserId') || '1';
        const params = { page: 1, size: 10, ryid: parseInt(userId) }
        const res = await TRJC.api.getTaskList(params)
        if (res.data.code === 200) {
          recentTasks.value = (res.data.data.list || []).map(item => mapTask(item))
        }
      } catch (error) {
        console.error('获取任务列表失败:', error)
      }
    };

    const fetchTaskStats = async () => {
      try {
        const res = await TRJC.api.getTaskStats()
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
    };

    const onSettings = () => {
      vant.showToast('打开设置');
    };

    const onStatClick = (type) => {
      const typeMap = {
        'pending': '待执行任务',
        'completed': '已完成任务',
        'toSubmit': '待提交数据'
      };
      vant.showToast(`查看${typeMap[type]}`);
    };

    const onTaskClick = (task) => {
      vant.showToast(`查看任务: ${task.title}`);
    };

    const viewAllTasks = () => {
      vant.showToast('查看全部任务');
    };

    Vue.onMounted(() => {
      fetchTaskList();
      fetchTaskStats();
    });

    return {
      user,
      taskStats,
      recentTasks,
      onSettings,
      onStatClick,
      onTaskClick,
      viewAllTasks
    };
  }
};

const HomeViewStyle = `
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
`;

export { HomeView, HomeViewStyle };
