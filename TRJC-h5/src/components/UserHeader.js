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
      <div class="top-nav animate-fade-in">
        <div class="nav-left">
          <van-icon name="wap-nav" size="22" color="#333" />
        </div>
        <span class="nav-title">耕地质量监测</span>
        <div class="nav-right">
          <div class="avatar-small" @click="onSettingsClick">{{ userInitial }}</div>
        </div>
      </div>
    </div>
  `,
  setup(props, { emit }) {
    const userInitial = Vue.computed(() => {
      return props.user.name ? props.user.name.charAt(props.user.name.length - 1) : 'U';
    });
    
    const onSettingsClick = () => {
      emit('settings');
    };
    
    return { userInitial, onSettingsClick };
  }
};

const UserHeaderStyle = `
.user-header {
  background: #F5F8FF;
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
  cursor: pointer;
}
`;

export { UserHeader, UserHeaderStyle };