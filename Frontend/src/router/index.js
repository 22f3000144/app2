import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Authorization/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
    
      // this generates a separate chunk (About.[hash].js) for this route

      component: () => import('../views/Authorization/LoginView.vue'),
    },
    {
      path: '/company-register',
      name: 'company-register',
    
      // this generates a separate chunk (About.[hash].js) for this route

      component: () => import('../views/Authorization/CompanyRegisterView.vue'),
    },
    {
      path: '/company-home',
      name: 'company-home',
      component: () => import('../views/Company/CompanyHomeView.vue'),
    },
    {
      path: '/company-drive',
      name: 'company-drive',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/Authorization/CreateDriveView.vue'),
    },
    {
      path: '/company-manage-drives',
      name: 'company-manage-drives',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/Authorization/ManageDriveView.vue'),
    },
    {
      path: '/company-profile',
      name: 'company-profile',
      component: () => import('../views/Company/CompanyProfileView.vue'),
    },
    {
      path: '/company-register',
      name: 'company-register',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/Authorization/CompanyRegisterView.vue'),
    },
    {
      path: '/company-shortlisted-students',
      name: 'company-shortlisted-students',
      component: () => import('../views/Company/ShortlistedStudentsView.vue'),
    },
    {
      path: '/student-register',
      name: 'student-register',
    
      // this generates a separate chunk (About.[hash].js) for this route

      component: () => import('../views/Authorization/StudentRegisterView.vue'),
    },
    {
    path: '/student-dashboard/:name',
    name: 'dashboard',
    component: () => import('../views/Student/StudentDashboardView.vue'),
    },
    {
    path: '/company-dashboard/:name',
    name: 'dashboard',
    component: () => import('../views/Company/CompanyDashboardView.vue'),
    },
    // Admin routes
    {
      path: '/admin',
      component: () => import('../views/Admin/AdminDashboardView.vue'),

      children: [

        {
          path: '',
          name: 'admin-home',
          component: () => import('../views/Admin/AdminHomeView.vue'),
        },

        {
          path: 'companies',
          name: 'manage-companies',
          component: () => import('../views/Admin/ManageCompaniesView.vue'),
        },

        {
          path: 'students',
          name: 'manage-students',
          component: () => import('../views/Admin/ManageStudentsView.vue'),
        },

        {
          path: 'drives',
          name: 'manage-drives',
          component: () => import('../views/Admin/ManageDrivesView.vue'),
        },

        {
          path: 'reports',
          name: 'reports',
          component: () => import('../views/Admin/ReportsView.vue'),
        },

        {
          path: 'profile',
          name: 'admin-profile',
          component: () => import('../views/Admin/AdminProfileView.vue'),
        },

      ]
    }

  ],
})

export default router
