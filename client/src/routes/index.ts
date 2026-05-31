import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useAuth } from '../store/auth'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/budget',
    name: 'Budget',
    component: () => import('../views/Budget.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/services',
    name: 'Services',
    component: () => import('../views/Service.vue'),
    meta: { requiresAuth: true }
  },
  
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Navigation Guard: Protect Routes & Handle Authentication Redirects
router.beforeEach((to, from, next) => {
  const authStore = useAuth()
  const isAuthenticated = authStore.authData // Assuming your Pinia store exposes this boolean

  // 1. If route requires authentication and user is NOT logged in -> Redirect to Login
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login' })
  }
  // 2. If route is for guests only (Login/Register) and user IS logged in -> Redirect to Dashboard
  else if (to.meta.requiresGuest && isAuthenticated) {
    next({ name: 'Dashboard' })
  }
  // 3. Otherwise, proceed normally
  else {
    next()
  }
})

export default router