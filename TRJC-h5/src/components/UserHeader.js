const UserHeader = {
  name: 'UserHeader',
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  template: `
    <div class="user-header">
      <div class="user-info">
        <div class="avatar">
          <img :src="user.avatar" alt="avatar">
        </div>
        <div class="user-details">
          <div class="user-name-row">
            <span class="user-name">{{ user.name }}</span>
            <span class="online-dot"></span>
          </div>
          <div class="user-role">{{ user.role }} · {{ user.district }}</div>
        </div>
      </div>
      <div class="settings-btn" @click="onSettingsClick">
        <van-icon name="setting-o" size="24" color="#fff" />
      </div>
    </div>
  `,
  setup(props, { emit }) {
    const onSettingsClick = () => {
      emit('settings');
    };
    
    return { onSettingsClick };
  }
};

const UserHeaderStyle = `
.user-header {
  background: var(--header-bg);
  padding: 20px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 0 0 20px 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid rgba(255, 255, 255, 0.3);
  flex-shrink: 0;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.user-name-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-name {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-white);
}

.online-dot {
  width: 10px;
  height: 10px;
  background-color: #4CD964;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.user-role {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.85);
}

.settings-btn {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.settings-btn:active {
  transform: scale(0.95);
  background: rgba(255, 255, 255, 0.3);
}
`;

export { UserHeader, UserHeaderStyle };
