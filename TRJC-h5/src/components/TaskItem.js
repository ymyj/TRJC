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
    <div :class="['task-item', 'animate-slide-in', \`list-item-\${index + 1}\`]" @click="onTaskClick">
      <div class="task-left-line"></div>
      <div class="task-card-content">
        <div class="task-header-row">
          <div class="task-title-row">
            <span class="task-title-text">{{ task.title }}</span>
            <span :class="['status-badge', getStatusClass(task.status)]">
              {{ task.statusLabel }}
            </span>
          </div>
        </div>
        <div class="task-info-grid">
          <div class="task-info-item">
            <van-icon name="label-o" size="14" color="#999" />
            <span class="info-label">任务编号：</span>
            <span class="info-value">{{ task.taskNo }}</span>
          </div>
          <div class="task-info-item">
            <van-icon name="calendar-o" size="14" color="#999" />
            <span class="info-label">采样时间：</span>
            <span class="info-value">{{ task.deadline }}</span>
          </div>
          <div class="task-info-item">
            <van-icon name="wap-home-o" size="14" color="#999" />
            <span class="info-label">任务类型：</span>
            <span class="info-value">{{ task.typeLabel }}</span>
          </div>
          <div class="task-info-item">
            <van-icon name="user-o" size="14" color="#999" />
            <span class="info-label">负责人：</span>
            <span class="info-value">{{ task.leader || '待分配' }}</span>
          </div>
        </div>
        <div class="task-actions-row">
          <div class="action-item" @click.stop="onViewDetail">
            <van-icon name="notes-o" size="16" />
            <span>任务详情</span>
          </div>
          <div class="action-item primary" @click.stop="onContinueSample">
            <van-icon name="replay" size="16" />
            <span>继续采样</span>
          </div>
        </div>
      </div>
    </div>
  `,
  setup(props, { emit }) {
    const getStatusClass = (status) => {
      const statusMap = {
        'pending': 'badge-pending',
        'in_progress': 'badge-in-progress',
        'completed': 'badge-completed'
      };
      return statusMap[status] || 'badge-pending';
    };
    
    const onViewDetail = () => {
      emit('detail', props.task);
    };
    
    const onContinueSample = () => {
      emit('continue', props.task);
    };
    
    const onTaskClick = () => {
      emit('click', props.task);
    };
    
    return { 
      getStatusClass, 
      onViewDetail,
      onContinueSample,
      onTaskClick 
    };
  }
};

const TaskItemStyle = `
.task-item {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  cursor: pointer;
  transition: all 0.3s ease;
  opacity: 0;
  display: flex;
  gap: 12px;
  position: relative;
  overflow: hidden;
}

.task-item:active {
  transform: scale(0.98);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.task-left-line {
  width: 4px;
  border-radius: 2px;
  background: linear-gradient(180deg, #4A90E2 0%, #5BA3F5 100%);
  flex-shrink: 0;
  align-self: stretch;
}

.task-card-content {
  flex: 1;
  min-width: 0;
}

.task-header-row {
  margin-bottom: 12px;
}

.task-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.task-title-text {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
  flex: 1;
}

.status-badge {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 12px;
  font-weight: 500;
  white-space: nowrap;
  flex-shrink: 0;
}

.badge-pending {
  background: #FFF3E0;
  color: #FF9500;
}

.badge-in-progress {
  background: #E3F2FD;
  color: #4A90E2;
}

.badge-completed {
  background: #E8F5E9;
  color: #34C759;
}

.task-info-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 14px;
}

.task-info-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
}

.info-label {
  color: #999;
  flex-shrink: 0;
}

.info-value {
  color: var(--text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.task-actions-row {
  display: flex;
  gap: 8px;
  border-top: 1px solid #F5F5F5;
  padding-top: 12px;
}

.action-item {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 12px;
  border-radius: 20px;
  font-size: 13px;
  color: #666;
  background: #F8F9FA;
  transition: all 0.2s ease;
}

.action-item:active {
  background: #EEEEEE;
}

.action-item.primary {
  background: #E3F2FD;
  color: #4A90E2;
}

.action-item.primary:active {
  background: #D0E8F7;
}
`;

export { TaskItem, TaskItemStyle };