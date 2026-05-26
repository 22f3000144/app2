<template>
  <div class="admin-dashboard">

    <!-- Sidebar -->
    <aside class="sidebar">

      <!-- Brand -->
      <div>

        <div class="brand">

          <div class="brand-logo">
                <img
      alt="App logo"
      class="logo"
      src="@/assets/logo.png"
      width="50"
      height="50"
    />
          </div>

          <div>
            <h2>Eduvora</h2>
            <p>Admin Panel</p>
          </div>

        </div>

        <!-- Menu -->
        <ul class="menu">

          <RouterLink
            to="/admin"
            class="menu-link"
          >
            <li>

              <div class="menu-item">

                <i class="bi bi-grid-fill"></i>

                <span>Dashboard</span>

              </div>

            </li>
          </RouterLink>

          <RouterLink
            to="/admin/companies"
            class="menu-link"
          >
            <li>

              <div class="menu-item">

                <i class="bi bi-buildings-fill"></i>

                <span>Companies</span>

              </div>

            </li>
          </RouterLink>

          <RouterLink
            to="/admin/students"
            class="menu-link"
          >
            <li>

              <div class="menu-item">

                <i class="bi bi-people-fill"></i>

                <span>Students</span>

              </div>

            </li>
          </RouterLink>

          <RouterLink
            to="/admin/drives"
            class="menu-link"
          >
            <li>

              <div class="menu-item">

                <i class="bi bi-briefcase-fill"></i>

                <span>Placement Drives</span>

              </div>

            </li>
          </RouterLink>

          <RouterLink
            to="/admin/reports"
            class="menu-link"
          >
            <li>

              <div class="menu-item">

                <i class="bi bi-bar-chart-fill"></i>

                <span>Reports</span>

              </div>

            </li>
          </RouterLink>

          <RouterLink
            to="/admin/profile"
            class="menu-link"
          >
            <li>

              <div class="menu-item">

                <i class="bi bi-person-circle"></i>

                <span>Profile</span>

              </div>

            </li>
          </RouterLink>

        </ul>

      </div>

      <!-- Logout -->
      <button
        class="logout-btn"
        @click="logout"
      >

        <i class="bi bi-box-arrow-right"></i>

        Logout

      </button>

    </aside>

    <!-- Main -->
    <main class="main-content">

      <!-- Topbar -->
      <div class="topbar">

        <!-- Left -->
        <div>

          <h3>
            Welcome Back, Admin 👋
          </h3>

          <p>
            Placement Management Dashboard
          </p>

        </div>

        <!-- Right -->
        <div class="topbar-right">

          <!-- Search -->
          <div class="search-box">

            <i class="bi bi-search"></i>

            <input
              type="text"
              placeholder="Search..."
              v-model="search"
            />

          </div>

          <!-- Admin -->
          <div class="admin-profile">

            <div class="admin-avatar">
              A
            </div>

            <div>

              <h6>Administrator</h6>

              <small>
                Admin Access
              </small>

            </div>

          </div>

        </div>

      </div>

      <!-- Dynamic Pages -->
      <div class="page-content">

        <RouterView />

      </div>

    </main>

  </div>
</template>

<script setup>
import { ref } from 'vue'

import {
  RouterLink,
  RouterView,
  useRouter,
} from 'vue-router'

const router = useRouter()

const search = ref('')

const logout = () => {

  localStorage.removeItem('token')

  localStorage.removeItem('user')

  router.push('/login')
}
</script>

<style scoped>
.admin-dashboard {
  display: flex;
  min-height: 100vh;
  background: #f1f5f9;
}

/* Sidebar */
.sidebar {
  width: 280px;
  background: #0f172a;
  color: white;

  padding: 24px 18px;

  display: flex;
  flex-direction: column;
  justify-content: space-between;

  position: sticky;
  top: 0;

  height: 100vh;
}

/* Brand */
.brand {
  display: flex;
  align-items: center;
  gap: 14px;

  margin-bottom: 45px;
}

.brand-logo {
  width: 52px;
  height: 52px;

  border-radius: 14px;

  background: #2563eb;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 24px;
  font-weight: 700;
}

.brand h2 {
  margin-bottom: 2px;
  font-size: 24px;
  font-weight: 700;
}

.brand p {
  color: #94a3b8;
  font-size: 14px;
  margin: 0;
}

/* Menu */
.menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu-link {
  text-decoration: none;
}

.menu li {
  margin-bottom: 12px;

  border-radius: 14px;

  transition: 0.3s;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 14px;

  padding: 14px 16px;

  color: #e2e8f0;

  font-weight: 500;
}

.menu-item i {
  font-size: 18px;
}

/* Active Route */
.router-link-active li {
  background: #1e293b;
}

.router-link-active .menu-item {
  color: white;
}

/* Hover */
.menu li:hover {
  background: #1e293b;
}

/* Logout */
.logout-btn {
  border: none;

  background: #dc2626;
  color: white;

  padding: 14px;

  border-radius: 14px;

  font-weight: 600;

  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;

  transition: 0.3s;
}

.logout-btn:hover {
  background: #b91c1c;
}

/* Main */
.main-content {
  flex: 1;

  padding: 28px;

  overflow-x: hidden;
}

/* Topbar */
.topbar {
  background: white;

  padding: 22px 26px;

  border-radius: 20px;

  margin-bottom: 25px;

  display: flex;
  justify-content: space-between;
  align-items: center;

  gap: 20px;
  flex-wrap: wrap;

  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.topbar h3 {
  margin-bottom: 5px;
  font-weight: 700;
}

.topbar p {
  margin: 0;
  color: #64748b;
}

/* Right */
.topbar-right {
  display: flex;
  align-items: center;
  gap: 20px;

  flex-wrap: wrap;
}

/* Search */
.search-box {
  position: relative;
}

.search-box i {
  position: absolute;

  top: 50%;
  left: 14px;

  transform: translateY(-50%);

  color: #94a3b8;
}

.search-box input {
  width: 260px;

  border: 1px solid #dbe2ea;
  outline: none;

  background: #f8fafc;

  padding: 12px 16px 12px 42px;

  border-radius: 12px;
}

/* Admin */
.admin-profile {
  display: flex;
  align-items: center;
  gap: 12px;
}

.admin-avatar {
  width: 48px;
  height: 48px;

  border-radius: 50%;

  background: #2563eb;
  color: white;

  display: flex;
  align-items: center;
  justify-content: center;

  font-weight: 700;
  font-size: 18px;
}

.admin-profile h6 {
  margin: 0;
  font-weight: 600;
}

.admin-profile small {
  color: #64748b;
}

/* Page */
.page-content {
  width: 100%;
}

/* Responsive */
@media (max-width: 992px) {

  .admin-dashboard {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    height: auto;

    position: relative;
  }

  .main-content {
    padding: 18px;
  }

  .menu {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }

  .menu li {
    margin-bottom: 0;
  }
}

@media (max-width: 576px) {

  .topbar {
    padding: 18px;
  }

  .topbar-right {
    width: 100%;
  }

  .search-box {
    width: 100%;
  }

  .search-box input {
    width: 100%;
  }

  .admin-profile {
    width: 100%;
  }

  .main-content {
    padding: 14px;
  }

  .brand {
    margin-bottom: 25px;
  }
}
</style>