const TaskItem = {
  name: 'TaskItem',
  props: {
    task: {
      type: Object,
      required: true
    },
    index: {
      type: Number,
      default: 0
    }
  },
  template: `
    <div :class="['task-item', 'animate-slide-in', `list-item-${index + 1}`]" @click="onTaskClick">
      <div class="task-header">
        <div class="task-title">{{ task.title }}</div>
        <span :class="['status-tag', getStatusClass(task.status)]">
          {{ task.statusLabel }}
        </span>
      </div>
      <div class="task-meta">
        <span class="task-no">任务编号：{{ task.taskNo }}</span>
        <span class="task-type">· {{ task.typeLabel }}</span>
      </div>
      <div class="task-footer">
        <div class="task-location">
          <van-icon name="location-o" size="14" color="#999" />
          <span>{{ task.location }}</span>
        </div>
        <div class="task-time" :class="{ 'urgent': isUrgent }">
          <van-icon name="clock-o" size="14" :color="isUrgent ? '#FF3B30' : '#999'" />
          <span>{{ timeLabel }}：{{ timeValue }}</span>
        </div>
      </div>
    </div>
  `,
  setup(props, { emit }) {
    const getStatusClass = (status) => {
      const statusMap = {
        'pending': 'status-pending',
        'in_progress': 'status-in-progress',
        'completed': 'status-completed',
        'to_submit': 'status-to-submit'
      };
      return statusMap[status] || 'status-pending';
    };
    
    const isUrgent = Vue.computed(() => {
      if (props.task.status === 'completed') return false;
      if (!props.task.deadline) return false;
      const deadline = new Date(props.task.deadline);
      const today = new Date();
      const diffDays = Math.ceil((deadline - today) / (1000 * 60 * 60 * 24));
      return diffDays <= 3;
    });
    
    const timeLabel = Vue.computed(() => {
      return props.task.status === 'completed' ? '完成' : '截止';
    });
    
    const timeValue = Vue.computed(() => {
      return props.task.status === 'completed' 
        ? props.task.completedAt 
        : props.task.deadline;
    });
    
    const onTaskClick = () => {
      emit('click', props.task);
    };
    
    return { 
      getStatusClass, 
      isUrgent, 
      timeLabel, 
      timeValue,
      onTaskClick 
    };
  }
};

const TaskItemStyle = `
.task-item {
  background: var(--card-bg);
  border-radius: var(--radius-md);
  padding: 16px;
  margin-bottom: 12px;
  box-shadow: var(--shadow-sm);
  cursor: pointer;
  transition: all 0.3s ease;
  opacity: 0;
}

.task-item:active {
  transform: scale(0.98);
  box-shadow: var(--shadow-md);
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.task-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  flex: 1;
  line-height: 1.4;
}

.task-meta {
  display: flex;
  gap: 4px;
  margin-bottom: 12px;
  font-size: 13px;
  color: var(--text-tertiary);
}

.task-no {
  color: var(--text-secondary);
}

.task-type {
  color: var(--text-tertiary);
}

.task-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  color: var(--text-tertiary);
}

.task-location {
  display: flex;
  align-items: center;
  gap: 4px;
}

.task-time {
  display: flex;
  align-items: center;
  gap: 4px;
}

.task-time.urgent span {
  color: var(--to-submit-color);
}
`;

export { TaskItem, TaskItemStyle };
