import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import Vant from 'vant'
import 'vant/lib/index.css'

import LoginView from './views/LoginView.js'
import HomeView from './views/HomeView.js'
import TaskListView from './views/TaskListView.js'
import SampleCollectionView from './views/SampleCollectionView.js'
import { BatchPlotSelectView, BatchPlotSelectViewStyle } from './views/BatchPlotSelectView.js'
import { BatchSampleFormView, BatchSampleFormViewStyle } from './views/BatchSampleFormView.js'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'Home',
    component: HomeView,
    meta: { requiresAuth: true }
  },
  {
    path: '/tasks',
    name: 'TaskList',
    component: TaskListView,
    meta: { requiresAuth: true }
  },
  {
    path: '/sample-collection/:taskId',
    name: 'SampleCollection',
    component: SampleCollectionView,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/batch-plot-select/:taskId',
    name: 'BatchPlotSelect',
    component: BatchPlotSelectView,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/batch-sample-form',
    name: 'BatchSampleForm',
    component: BatchSampleFormView,
    meta: { requiresAuth: true },
    props: (route) => ({
      taskId: route.query.taskId
    })
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

const app = createApp({})

app.use(router)
app.use(Vant)

const styleEl = document.createElement('style')
styleEl.textContent = `
${BatchPlotSelectViewStyle}
${BatchSampleFormViewStyle}
`
document.head.appendChild(styleEl)

app.mount('#app')
