<template>
  <aside class="sidebar">
    <div class="logo">耕地质量监测管理系统</div>
    
    <div class="menu-section">
      <div class="menu-title">任务管理</div>
      <router-link 
        to="/tasks" 
        class="menu-item" 
        :class="{ active: activeMenu === 'tasks' }"
      >
        <span class="menu-icon">+</span>
        <span>任务发布</span>
      </router-link>
    </div>

    <div class="menu-section">
      <div class="menu-title">资产管理</div>
      <router-link 
        to="/personnel" 
        class="menu-item" 
        :class="{ active: activeMenu === 'personnel' }"
      >
        <span class="menu-icon">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
        </span>
        <span>人员管理</span>
      </router-link>
    </div>

    <div class="menu-section">
      <div class="menu-title">档案中心</div>
      <router-link 
        to="/dataset" 
        class="menu-item" 
        :class="{ active: activeMenu === 'dataset' }"
      >
        <span class="menu-icon">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
          </svg>
        </span>
        <span>耕地质量数据集</span>
      </router-link>
      <router-link 
        to="/map" 
        class="menu-item" 
        :class="{ active: activeMenu === 'map' }"
      >
        <span class="menu-icon">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="1 6 1 22 8 18 16 22 21 18 21 2 16 6 8 2 1 6"></polygon>
            <line x1="8" y1="2" x2="8" y2="18"></line>
            <line x1="16" y1="6" x2="16" y2="22"></line>
          </svg>
        </span>
        <span>地块管理</span>
      </router-link>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  activeMenu: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.sidebar {
  width: 240px;
  background-color: #fff;
  border-right: 1px solid #e8e8e8;
  padding: 20px 0;
  flex-shrink: 0;
}

.logo {
  padding: 0 24px 24px;
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  border-bottom: 1px solid #f0f0f0;
  margin-bottom: 16px;
}

.menu-section {
  margin-bottom: 8px;
}

.menu-title {
  padding: 12px 24px;
  font-size: 13px;
  color: #8c8c8c;
  font-weight: 500;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 12px 24px;
  margin: 0 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  color: #595959;
  font-size: 14px;
  text-decoration: none;
}

.menu-item:hover {
  background-color: #f5f5f5;
  color: #262626;
}

.menu-item.active {
  background-color: #e6f4ff;
  color: #1677ff;
  border: 1px solid #1677ff;
}

.menu-icon {
  width: 18px;
  height: 18px;
  margin-right: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
