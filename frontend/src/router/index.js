import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import LoginView from '../views/LoginView.vue'
import UserDashboardView from '../views/UserDashboardView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/login' },
    { path: '/login', component: LoginView },
    { path: '/dashboard', component: UserDashboardView, meta: { requiresAuth: true } },
    // Add Admin Dash later
  ]
})

// Navigation Guard: Protect routes!
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  
  if (to.meta.requiresAuth && !auth.user) {
    next('/login') // Kick them to login if not authenticated
  } else if (to.path === '/login' && auth.user) {
    next('/dashboard') // Send to dash if already logged in
  } else {
    next() // Let them proceed
  }
})

export default router