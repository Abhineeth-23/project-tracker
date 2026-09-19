import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import LoginView from '../views/LoginView.vue'
import UserDashboardView from '../views/UserDashboardView.vue'
import AdminDashboardView from '../views/AdminDashboardView.vue'
import AdminCompanySelectView from '../views/AdminCompanySelectView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/login' },
    { path: '/login', component: LoginView },
    { path: '/dashboard', component: UserDashboardView, meta: { requiresAuth: true } },
    { path: '/admin/select-company', name: 'admin-select-company', component: AdminCompanySelectView, meta: { requiresAdmin: true } },
    { path: '/admin', name: 'admin', component: AdminDashboardView, meta: { requiresAdmin: true } }
  ]
})

// Navigation Guard: Protect routes!
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  const isAdminOrViewer = auth.user && (auth.user.role === 'admin' || auth.user.role === 'viewer')
  
  if (to.meta.requiresAdmin) {
    if (!auth.user) {
      next('/login')
    } else if (!isAdminOrViewer) {
      next('/dashboard')
    } else {
      next()
    }
  } else if (to.meta.requiresAuth) {
    if (!auth.user) {
      next('/login')
    } else {
      next()
    }
  } else if (to.path === '/login' && auth.user) {
    if (isAdminOrViewer) {
      next('/admin/select-company')
    } else {
      next('/dashboard')
    }
  } else {
    next()
  }
})

export default router