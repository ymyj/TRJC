<template>
  <div class="app-container">
    <Sidebar v-if="showSidebar" :active-menu="activeMenu" />
    <main class="main-content" :class="{ 'full-width': !showSidebar }">
      <div v-if="showSidebar" class="header">
        <div class="header-left"></div>
        <div class="header-right">
          <div class="user-info" @click="showDropdown = !showDropdown">
            <div class="user-avatar">{{ userInfo.XM?.charAt(0) || '用' }}</div>
            <span class="user-name">{{ userInfo.XM || '用户' }}</span>
            <span class="dropdown-arrow">▼</span>
          </div>
          <div v-if="showDropdown" class="dropdown-menu">
            <div class="dropdown-item" @click="handleLogout">
              <span class="dropdown-icon">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                  <polyline points="16 17 21 12 16 7"></polyline>
                  <line x1="21" y1="12" x2="9" y2="12"></line>
                </svg>
              </span>
              退出登录
            </div>
          </div>
        </div>
      </div>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
import { logout } from './api/auth'

const route = useRoute()
const router = useRouter()
const activeMenu = computed(() => route.meta.activeMenu || '')
const showSidebar = computed(() => route.path !== '/login')
const showDropdown = ref(false)

const userInfo = ref({
  XM: '',
  LXFS: '',
  GW: ''
})

const loadUserInfo = () => {
  const info = localStorage.getItem('userInfo')
  if (info) {
    try {
      userInfo.value = JSON.parse(info)
    } catch (e) {
      console.error('解析用户信息失败', e)
    }
  }
}

const handleLogout = async () => {
  try {
    await logout()
  } catch (e) {
    console.error('退出登录API调用失败', e)
  } finally {
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
    router.push('/login')
  }
}

const handleClickOutside = (e) => {
  if (!e.target.closest('.header-right')) {
    showDropdown.value = false
  }
}

onMounted(() => {
  loadUserInfo()
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.app-container {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  background-color: #f5f7fa;
}

.main-content.full-width {
  padding: 0;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  height: 60px;
  background-color: #fff;
  border-bottom: 1px solid #e8e8e8;
}

.header-right {
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 8px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: #f5f5f5;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
}

.user-name {
  font-size: 14px;
  color: #262626;
  font-weight: 500;
}

.dropdown-arrow {
  font-size: 10px;
  color: #8c8c8c;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  min-width: 120px;
  z-index: 1000;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  font-size: 14px;
  color: #595959;
  cursor: pointer;
  transition: background-color 0.3s;
}

.dropdown-item:hover {
  background-color: #f5f5f5;
  color: #ff4d4f;
}

.dropdown-icon {
  display: flex;
  align-items: center;
}
</style>
