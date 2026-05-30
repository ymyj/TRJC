const TaskStats = {
  name: 'TaskStats',
  props: {
    stats: {
      type: Object,
      required: true
    }
  },
  template: `
    <div class="task-stats-section">
      <div class="section-label">
        <span class="label-bar"></span>
        <span class="label-text">今日任务统计</span>
      </div>
      <div class="stats-grid">
        <div class="stat-card stat-card-inprogress" @click="onStatClick('in_progress')">
          <div class="stat-icon-wrapper">
            <van-icon name="replay" size="20" color="#4A90E2" />
          </div>
          <div class="stat-content">
            <span class="stat-title">进行中</span>
            <span class="stat-value">{{ stats.inProgress }}</span>
          </div>
        </div>
        <div class="stat-card stat-card-completed" @click="onStatClick('completed')">
          <div class="stat-icon-wrapper">
            <van-icon name="checked" size="20" color="#34C759" />
          </div>
          <div class="stat-content">
            <span class="stat-title">已完成</span>
            <span class="stat-value">{{ stats.completed }}</span>
          </div>
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
.task-stats-section {
  margin: 0 16px 16px;
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

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.stat-card {
  background: #fff;
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
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

.stat-card-pending .stat-icon-wrapper {
  background: #FFF3E0;
}

.stat-card-completed .stat-icon-wrapper {
  background: #E8F5E9;
}

.stat-card-submit .stat-icon-wrapper {
  background: #FFEBEE;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.stat-title {
  font-size: 12px;
  color: #999;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #1A1A1A;
  line-height: 1.1;
}
`;

export { TaskStats, TaskStatsStyle };