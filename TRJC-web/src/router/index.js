import { createRouter, createWebHashHistory } from 'vue-router'
import Login from '../views/Login.vue'
import TaskList from '../views/TaskList.vue'
import TaskPublish from '../views/TaskPublish.vue'
import TaskDetail from '../views/TaskDetail.vue'
import LandDetail from '../views/LandDetail.vue'
import PersonnelManagement from '../views/PersonnelManagement.vue'
import MapManagement from '../views/MapManagement.vue'
import FarmlandDataset from '../views/FarmlandDataset.vue'
import PlotAdd from '../views/PlotAdd.vue'
import PlotDetail from '../views/PlotDetail.vue'
import TaskAssign from '../views/TaskAssign.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false, title: '登录' }
  },
  {
    path: '/',
    redirect: '/tasks'
  },
  {
    path: '/tasks',
    name: 'TaskList',
    component: TaskList,
    meta: { title: '任务列表', activeMenu: 'tasks' }
  },
  {
    path: '/tasks/publish',
    name: 'TaskPublish',
    component: TaskPublish,
    meta: { title: '任务发布', activeMenu: 'tasks' }
  },
  {
    path: '/tasks/detail/:id',
    name: 'TaskDetail',
    component: TaskDetail,
    meta: { title: '任务详情', activeMenu: 'tasks' }
  },
  {
    path: '/land/detail/:id',
    name: 'LandDetail',
    component: LandDetail,
    meta: { title: '采样地块详情', activeMenu: 'tasks' }
  },
  {
    path: '/tasks/assign/:id',
    name: 'TaskAssign',
    component: TaskAssign,
    meta: { title: '任务分配', activeMenu: 'tasks' }
  },
  {
    path: '/personnel',
    name: 'PersonnelManagement',
    component: PersonnelManagement,
    meta: { title: '人员管理', activeMenu: 'personnel' }
  },
  {
    path: '/map',
    name: 'MapManagement',
    component: MapManagement,
    meta: { title: '地块管理', activeMenu: 'map' }
  },
  {
    path: '/map/plot/add',
    name: 'PlotAdd',
    component: PlotAdd,
    meta: { title: '新增图斑', activeMenu: 'map' }
  },
  {
    path: '/map/plot/detail/:id',
    name: 'PlotDetail',
    component: PlotDetail,
    meta: { title: '图斑详情', activeMenu: 'map' }
  },
  {
    path: '/dataset',
    name: 'FarmlandDataset',
    component: FarmlandDataset,
    meta: { title: '耕地质量数据集', activeMenu: 'dataset' }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth === false) {
    if (token && to.path === '/login') {
      next('/')
    } else {
      next()
    }
  } else {
    if (token) {
      next()
    } else {
      next('/login')
    }
  }
})

export default router
