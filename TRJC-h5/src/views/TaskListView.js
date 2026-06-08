import { useRouter } from 'vue-router';

export const TaskListView = {
  name: 'TaskListView',
  emits: ['navigate'],
  props: {
    userId: {
      type: String,
      default: ''
    },
    ryid: {
      type: [String, Number],
      default: null
    }
  },
  setup(props, { emit }) {
    const router = useRouter();
    const tasks = Vue.ref([]);
    const loading = Vue.ref(true);
    const searchQuery = Vue.ref('');
    const showStatusFilter = Vue.ref(false);
    const selectedStatus = Vue.ref('');

    const statusMap = {
      pending: '待领取',
      survey_done: '勘察完成',
      sampling_done: '采样完成',
      completed: '已完成'
    };

    const filteredTasks = Vue.computed(() => {
      let result = tasks.value;
      if (searchQuery.value) {
        result = result.filter(t => (t.TBH || '').includes(searchQuery.value));
      }
      if (selectedStatus.value) {
        result = result.filter(t => t.status === selectedStatus.value);
      }
      return result;
    });

    const goBack = () => {
      emit('navigate', 'home');
    };

    const fetchTasks = async () => {
      try {
        loading.value = true;
        const res = await TRJC.api.getTaskList({
          user_id: props.userId,
          ryid: props.ryid
        });
        if (res.data.code === 200) {
          tasks.value = res.data.data || [];
        }
      } catch (error) {
        console.error('获取任务列表失败:', error);
      } finally {
        loading.value = false;
      }
    };

    const viewTaskDetail = (task) => {
      emit('navigate', 'plot-list', {
        taskId: task.ID,
        taskName: task.TBH || '任务' + task.ID,
        taskStatus: task.status
      });
    };

    const batchCollect = (task) => {
      router.push({
        path: '/batch-plot-select/' + task.ID
      });
    };

    Vue.onMounted(() => {
      fetchTasks();
    });

    return {
      tasks,
      loading,
      searchQuery,
      showStatusFilter,
      selectedStatus,
      statusMap,
      filteredTasks,
      goBack,
      viewTaskDetail,
      batchCollect
    };
  },
  template: `
    <div class="task-list-view">
      <div class="task-list-header">
        <div class="task-list-header-back" @click="goBack">
          <van-icon name="arrow-left" size="20" color="#fff" />
        </div>
        <span class="task-list-header-title">任务列表</span>
      </div>

      <div class="task-list-search">
        <van-search v-model="searchQuery" placeholder="请输入图斑编号" shape="round" background="#f5f5f5" />
      </div>

      <div class="task-list-content">
        <div v-if="loading" class="loading-state">
          <van-loading size="24px">加载中...</van-loading>
        </div>
        
        <div v-else-if="filteredTasks.length === 0" class="empty-state">
          <van-icon name="search" size="48" color="#DDD" />
          <p>暂无任务</p>
        </div>
        
        <div v-else class="task-list">
          <div v-for="task in filteredTasks" :key="task.ID" class="task-card">
            <div class="task-card-header">
              <span class="task-card-title">{{ task.TBH || '任务' + task.ID }}</span>
              <span class="task-card-status" :class="'status-' + task.status">
                {{ statusMap[task.status] || task.status }}
              </span>
            </div>
            <div class="task-card-body">
              <div class="task-info-row">
                <span class="task-info-label">图斑编号:</span>
                <span class="task-info-value">{{ task.TBH }}</span>
              </div>
              <div class="task-info-row">
                <span class="task-info-label">所属区划:</span>
                <span class="task-info-value">{{ task.SSQH }}</span>
              </div>
              <div class="task-info-row">
                <span class="task-info-label">面积:</span>
                <span class="task-info-value">{{ task.TBMJ }}㎡</span>
              </div>
            </div>
            <div class="task-card-footer">
              <button class="task-btn batch-btn" @click.stop="batchCollect(task)">批量采集</button>
              <button class="task-btn detail-btn" @click.stop="viewTaskDetail(task)">查看详情</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
};

export const TaskListViewStyle = `
.task-list-view {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.task-list-header {
  background: linear-gradient(135deg, #5B9FE8 0%, #4A90E2 50%, #3D7FD4 100%);
  padding: 16px;
  display: flex;
  align-items: center;
  position: relative;
  border-radius: 0 0 20px 20px;
}

.task-list-header-back {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.task-list-header-back:active {
  background: rgba(255, 255, 255, 0.2);
}

.task-list-header-title {
  flex: 1;
  text-align: center;
  font-size: 18px;
  font-weight: 600;
  color: #fff;
  margin-right: 36px;
}

.task-list-search {
  padding: 12px 16px;
  background: #f5f5f5;
}

.task-list-content {
  padding: 0 16px 16px;
}

.loading-state, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #999;
}

.empty-state p {
  margin-top: 12px;
  font-size: 14px;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.task-card {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.task-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.task-card-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.task-card-status {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 12px;
}

.status-pending {
  background: #FFF3E0;
  color: #F57C00;
}

.status-survey_done {
  background: #E3F2FD;
  color: #1565C0;
}

.status-sampling_done {
  background: #E8F5E9;
  color: #2E7D32;
}

.status-completed {
  background: #F3E5F5;
  color: #7B1FA2;
}

.task-card-body {
  margin-bottom: 12px;
}

.task-info-row {
  display: flex;
  margin-bottom: 6px;
  font-size: 13px;
}

.task-info-row:last-child {
  margin-bottom: 0;
}

.task-info-label {
  color: #999;
  width: 70px;
  flex-shrink: 0;
}

.task-info-value {
  color: #333;
}

.task-card-footer {
  display: flex;
  gap: 12px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

.task-btn {
  flex: 1;
  height: 36px;
  border: none;
  border-radius: 18px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.batch-btn {
  background: #E3F2FD;
  color: #1565C0;
}

.batch-btn:active {
  background: #BBDEFB;
}

.detail-btn {
  background: #4A90E2;
  color: #fff;
}

.detail-btn:active {
  opacity: 0.9;
}
`;
