import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Navigation Guard: Protect Routes & Handle Authentication Redirects
// router.beforeEach((to, from, next) => {
//   const authStore = useAuthStore()
//   const isAuthenticated = authStore.isAuthenticated // Assuming your Pinia store exposes this boolean

//   // 1. If route requires authentication and user is NOT logged in -> Redirect to Login
//   if (to.meta.requiresAuth && !isAuthenticated) {
//     next({ name: 'Login' })
//   }
//   // 2. If route is for guests only (Login/Register) and user IS logged in -> Redirect to Dashboard
//   else if (to.meta.requiresGuest && isAuthenticated) {
//     next({ name: 'Dashboard' })
//   }
//   // 3. Otherwise, proceed normally
//   else {
//     next()
//   }
// })

export default router