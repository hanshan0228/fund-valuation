import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/portfolios'
  },
  {
    path: '/portfolios',
    name: 'PortfolioList',
    component: () => import('../views/PortfolioList.vue')
  },
  {
    path: '/portfolios/:id',
    name: 'PortfolioDetail',
    component: () => import('../views/PortfolioDetail.vue')
  },
  {
    path: '/upload',
    name: 'UploadOCR',
    component: () => import('../views/UploadOCR.vue')
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: () => import('../views/Statistics.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
