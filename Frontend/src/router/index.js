import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Authorization/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [

    // =========================
    // HOME
    // =========================
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },

    // =========================
    // AUTH ROUTES
    // =========================
    {
      path: '/login',
      name: 'login',
      component: () =>
        import('../views/Authorization/LoginView.vue'),
    },

    {
      path: '/company-register',
      name: 'company-register',
      component: () =>
        import('../views/Authorization/CompanyRegisterView.vue'),
    },

    {
      path: '/student-register',
      name: 'student-register',
      component: () =>
        import('../views/Authorization/StudentRegisterView.vue'),
    },

    // =========================
    // COMPANY DASHBOARD
    // =========================
    {
      path: '/company-dashboard/:name',
      component: () =>
        import('../views/Company/CompanyDashboardView.vue'),

      children: [

        {
          path: '',
          name: 'company-home',
          component: () =>
            import('../views/Company/CompanyHomeView.vue'),
        },

        {
          path: 'create-drive',
          name: 'company-drive',
          component: () =>
            import('../views/Company/CreateDriveView.vue'),
        },

        {
          path: 'manage-drives',
          name: 'company-manage-drives',
          component: () =>
            import('../views/Company/ManageDriveView.vue'),
        },

        {
          path: 'profile',
          name: 'company-profile',
          component: () =>
            import('../views/Company/CompanyProfileView.vue'),
        },

        {
          path: 'shortlisted-students',
          name: 'company-shortlisted-students',
          component: () =>
            import('../views/Company/ShortlistedStudentsView.vue'),
        },

        {
          path: 'applicants/:id',
          name: 'company-applicants',
          component: () =>
            import('../views/Company/ApplicantsView.vue'),
        }

      ]
    },

    // =========================
    // STUDENT DASHBOARD
    // =========================
    {
      path: '/student-dashboard/:name',
      name: 'student-dashboard',
      component: () =>
        import('../views/Student/StudentDashboardView.vue'),
    },

    // =========================
    // ADMIN DASHBOARD
    // =========================
    {
      path: '/admin',
      component: () =>
        import('../views/Admin/AdminDashboardView.vue'),

      children: [

        {
          path: '',
          name: 'admin-home',
          component: () =>
            import('../views/Admin/AdminHomeView.vue'),
        },

        {
          path: 'companies',
          name: 'manage-companies',
          component: () =>
            import('../views/Admin/ManageCompaniesView.vue'),
        },

        {
          path: 'students',
          name: 'manage-students',
          component: () =>
            import('../views/Admin/ManageStudentsView.vue'),
        },

        {
          path: 'drives',
          name: 'manage-drives',
          component: () =>
            import('../views/Admin/ManageDrivesView.vue'),
        },

        {
          path: 'reports',
          name: 'reports',
          component: () =>
            import('../views/Admin/ReportsView.vue'),
        },

        {
          path: 'profile',
          name: 'admin-profile',
          component: () =>
            import('../views/Admin/AdminProfileView.vue'),
        },

      ]
    }

  ],
})


// // =========================
// // GLOBAL ROUTE GUARD
// // =========================
// router.beforeEach((to, from) => {

//   const token = localStorage.getItem('token')
//   const role = localStorage.getItem('role')

//   const publicRoutes = ['home', 'login', 'company-register/:name', 'student-register/:name']

//   // Not logged in → redirect
//   if (!token && !publicRoutes.includes(to.name)) {
//     return { name: 'login' }
//   }

//   // Admin protection
//   if (to.path.startsWith('/admin') && role !== 'admin') {
//     return { name: 'login' }
//   }

//   // Company protection
//   if (to.path.startsWith('/company-dashboard') && role !== 'company') {
//     return { name: 'login' }
//   }

//   // Student protection
//   if (to.path.startsWith('/student-dashboard') && role !== 'student') {
//     return { name: 'login' }
//   }

//   // Allow navigation
//   return true
// })

export default router