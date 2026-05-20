const TaskStats = {
  name: 'TaskStats',
  props: {
    stats: {
      type: Object,
      required: true
    }
  },
  template: `
    <div class="task-stats-card animate-fade-in">
      <div class="stats-title">今日任务统计</div>
      <div class="stats-grid">
        <div class="stat-item" @click="onStatClick('pending')">
          <div class="stat-number" style="color: var(--pending-color)">{{ stats.pending }}</div>
          <div class="stat-label">待执行任务</div>
        </div>
        <div class="stat-item" @click="onStatClick('completed')">
          <div class="stat-number" style="color: var(--completed-color)">{{ stats.completed }}</div>
          <div class="stat-label">已完成任务</div>
        </div>
        <div class="stat-item" @click="onStatClick('toSubmit')">
          <div class="stat-number" style="color: var(--to-submit-color)">{{ stats.toSubmit }}</div>
          <div class="stat-label">待提交数据</div>
        </div>
      </div>
    </div>
  `,
  setup(props, { emit }) {
    const onStatClick = (type) => {
      emit('click', type);
    };
    
    return { onStatClick };
  }
};

const TaskStatsStyle = `
.task-stats-card {
  background: var(--card-bg);
  border-radius: var(--radius-md);
  margin: 12px 16px;
  padding: 16px;
  box-shadow: var(--shadow-sm);
}

.stats-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 16px;
}

.stats-grid {
  display: flex;
  justify-content: space-around;
  gap: 12px;
}

.stat-item {
  flex: 1;
  text-align: center;
  padding: 16px 8px;
  background: #FAFAFA;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.3s ease;
}

.stat-item:active {
  transform: scale(0.98);
  background: #F0F0F0;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
}
`;

export { TaskStats, TaskStatsStyle };
