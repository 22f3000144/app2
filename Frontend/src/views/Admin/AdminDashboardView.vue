<template>
  <div class="admin-dashboard">

    <!-- Sidebar -->
    <aside class="sidebar">

      <div>

        <div class="brand">
          <h2>Eduvora</h2>
          <p>Admin Dashboard</p>
        </div>

        <ul class="menu">

          <li
            :class="{ active: activeMenu === 'dashboard' }"
            @click="activeMenu = 'dashboard'"
          >
            <i class="bi bi-grid-fill"></i>
            Dashboard
          </li>

          <li
            :class="{ active: activeMenu === 'companies' }"
            @click="activeMenu = 'companies'"
          >
            <i class="bi bi-buildings-fill"></i>
            Companies
          </li>

          <li
            :class="{ active: activeMenu === 'students' }"
            @click="activeMenu = 'students'"
          >
            <i class="bi bi-people-fill"></i>
            Students
          </li>

          <li
            :class="{ active: activeMenu === 'drives' }"
            @click="activeMenu = 'drives'"
          >
            <i class="bi bi-briefcase-fill"></i>
            Placement Drives
          </li>

          <li
            :class="{ active: activeMenu === 'applications' }"
            @click="activeMenu = 'applications'"
          >
            <i class="bi bi-file-earmark-text-fill"></i>
            Applications
          </li>

        </ul>

      </div>

      <button class="logout-btn" @click="logout">
        Logout
      </button>

    </aside>

    <!-- Main Content -->
    <main class="main-content">

      <!-- Navbar -->
      <div class="topbar">

        <div>
          <h3>Welcome Admin</h3>
          <p>Placement Portal Management Panel</p>
        </div>

        <div class="search-box">
          <input
            type="text"
            placeholder="Search..."
            v-model="search"
          />
        </div>

      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-box">
        Loading Dashboard...
      </div>

      <div v-else>

        <!-- Dashboard -->
        <section v-if="activeMenu === 'dashboard'">

          <div class="stats-grid">

            <div class="stat-card">
              <h5>Total Students</h5>
              <h2>{{ students.length }}</h2>
            </div>

            <div class="stat-card">
              <h5>Total Companies</h5>
              <h2>{{ companies.length }}</h2>
            </div>

            <div class="stat-card">
              <h5>Total Drives</h5>
              <h2>{{ drives.length }}</h2>
            </div>

            <div class="stat-card">
              <h5>Total Applications</h5>
              <h2>{{ applications.length }}</h2>
            </div>

          </div>

          <!-- Recent Drives -->
          <div class="section-card">

            <div class="section-header">
              <h4>Recent Placement Drives</h4>
            </div>

            <div v-if="drives.length === 0" class="empty-box">
              <i class="bi bi-briefcase"></i>
              <h5>No Placement Drives Found</h5>
            </div>

            <div v-else class="table-responsive">

              <table class="table custom-table">

                <thead>
                  <tr>
                    <th>Company</th>
                    <th>Role</th>
                    <th>Status</th>
                    <th>Deadline</th>
                  </tr>
                </thead>

                <tbody>

                  <tr
                    v-for="drive in drives.slice(0, 5)"
                    :key="drive.id"
                  >
                    <td>{{ drive.company_name }}</td>
                    <td>{{ drive.job_title }}</td>

                    <td>
                      <span
                        class="status-badge"
                        :class="drive.status.toLowerCase()"
                      >
                        {{ drive.status }}
                      </span>
                    </td>

                    <td>{{ drive.deadline }}</td>
                  </tr>

                </tbody>

              </table>

            </div>

          </div>

        </section>

        <!-- Companies -->
        <section v-if="activeMenu === 'companies'">

          <div class="section-card">

            <div class="section-header">
              <h4>Registered Companies</h4>
            </div>

            <div v-if="companies.length === 0" class="empty-box">
              <i class="bi bi-buildings"></i>
              <h5>No Companies Found</h5>
            </div>

            <div v-else class="table-responsive">

              <table class="table custom-table">

                <thead>
                  <tr>
                    <th>Company</th>
                    <th>Email</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>

                <tbody>

                  <tr
                    v-for="company in filteredCompanies"
                    :key="company.id"
                  >

                    <td>{{ company.company_name }}</td>

                    <td>{{ company.email }}</td>

                    <td>
                      <span
                        class="status-badge"
                        :class="company.status.toLowerCase()"
                      >
                        {{ company.status }}
                      </span>
                    </td>

                    <td>

                      <button
                        class="approve-btn"
                        @click="approveCompany(company.id)"
                      >
                        Approve
                      </button>

                      <button
                        class="reject-btn"
                        @click="rejectCompany(company.id)"
                      >
                        Reject
                      </button>

                    </td>

                  </tr>

                </tbody>

              </table>

            </div>

          </div>

        </section>

        <!-- Students -->
        <section v-if="activeMenu === 'students'">

          <div class="section-card">

            <div class="section-header">
              <h4>Students</h4>
            </div>

            <div v-if="students.length === 0" class="empty-box">
              <i class="bi bi-people"></i>
              <h5>No Students Found</h5>
            </div>

            <div v-else class="table-responsive">

              <table class="table custom-table">

                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Branch</th>
                    <th>CGPA</th>
                  </tr>
                </thead>

                <tbody>

                  <tr
                    v-for="student in filteredStudents"
                    :key="student.id"
                  >

                    <td>{{ student.name }}</td>
                    <td>{{ student.email }}</td>
                    <td>{{ student.branch }}</td>
                    <td>{{ student.cgpa }}</td>

                  </tr>

                </tbody>

              </table>

            </div>

          </div>

        </section>

        <!-- Drives -->
        <section v-if="activeMenu === 'drives'">

          <div class="section-card">

            <div class="section-header">
              <h4>Placement Drives</h4>
            </div>

            <div v-if="drives.length === 0" class="empty-box">
              <i class="bi bi-briefcase"></i>
              <h5>No Drives Found</h5>
            </div>

            <div v-else class="table-responsive">

              <table class="table custom-table">

                <thead>
                  <tr>
                    <th>Company</th>
                    <th>Role</th>
                    <th>Deadline</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>

                <tbody>

                  <tr
                    v-for="drive in filteredDrives"
                    :key="drive.id"
                  >

                    <td>{{ drive.company_name }}</td>

                    <td>{{ drive.job_title }}</td>

                    <td>{{ drive.deadline }}</td>

                    <td>
                      <span
                        class="status-badge"
                        :class="drive.status.toLowerCase()"
                      >
                        {{ drive.status }}
                      </span>
                    </td>

                    <td>

                      <button
                        class="approve-btn"
                        @click="approveDrive(drive.id)"
                      >
                        Approve
                      </button>

                      <button
                        class="reject-btn"
                        @click="rejectDrive(drive.id)"
                      >
                        Reject
                      </button>

                    </td>

                  </tr>

                </tbody>

              </table>

            </div>

          </div>

        </section>

        <!-- Applications -->
        <section v-if="activeMenu === 'applications'">

          <div class="section-card">

            <div class="section-header">
              <h4>Applications</h4>
            </div>

            <div v-if="applications.length === 0" class="empty-box">
              <i class="bi bi-file-earmark"></i>
              <h5>No Applications Found</h5>
            </div>

            <div v-else class="table-responsive">

              <table class="table custom-table">

                <thead>
                  <tr>
                    <th>Student</th>
                    <th>Company</th>
                    <th>Role</th>
                    <th>Status</th>
                  </tr>
                </thead>

                <tbody>

                  <tr
                    v-for="application in applications"
                    :key="application.id"
                  >

                    <td>{{ application.student_name }}</td>

                    <td>{{ application.company_name }}</td>

                    <td>{{ application.job_title }}</td>

                    <td>
                      <span
                        class="status-badge"
                        :class="application.status.toLowerCase()"
                      >
                        {{ application.status }}
                      </span>
                    </td>

                  </tr>

                </tbody>

              </table>

            </div>

          </div>

        </section>

      </div>

    </main>

  </div>
</template>

<script setup>
import axios from 'axios'
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const loading = ref(true)

const activeMenu = ref('dashboard')

const search = ref('')

const students = ref([])

const companies = ref([])

const drives = ref([])

const applications = ref([])

const fetchDashboard = async () => {

  try {

    const token = localStorage.getItem('token')

    // Students
    const studentsResponse = await axios.get(
      'http://127.0.0.1:5000/api/admin/students',
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    students.value = studentsResponse.data || []

    // Companies
    const companiesResponse = await axios.get(
      'http://127.0.0.1:5000/api/admin/companies',
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    companies.value = companiesResponse.data || []

    // Drives
    const drivesResponse = await axios.get(
      'http://127.0.0.1:5000/api/admin/drives',
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    drives.value = drivesResponse.data || []

    // Applications
    const applicationsResponse = await axios.get(
      'http://127.0.0.1:5000/api/admin/applications',
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    applications.value = applicationsResponse.data || []

  } catch (error) {

    console.log(error)

  } finally {

    loading.value = false
  }
}

onMounted(() => {
  fetchDashboard()
})

const filteredCompanies = computed(() => {

  return companies.value.filter((company) => {

    return (
      company.company_name
        ?.toLowerCase()
        .includes(search.value.toLowerCase())
    )
  })
})

const filteredStudents = computed(() => {

  return students.value.filter((student) => {

    return (
      student.name
        ?.toLowerCase()
        .includes(search.value.toLowerCase())
    )
  })
})

const filteredDrives = computed(() => {

  return drives.value.filter((drive) => {

    return (
      drive.job_title
        ?.toLowerCase()
        .includes(search.value.toLowerCase())
    )
  })
})

const approveCompany = async (companyId) => {

  try {

    const token = localStorage.getItem('token')

    await axios.put(
      `http://127.0.0.1:5000/api/admin/company/approve/${companyId}`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    fetchDashboard()

  } catch (error) {

    console.log(error)
  }
}

const rejectCompany = async (companyId) => {

  try {

    const token = localStorage.getItem('token')

    await axios.put(
      `http://127.0.0.1:5000/api/admin/company/reject/${companyId}`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    fetchDashboard()

  } catch (error) {

    console.log(error)
  }
}

const approveDrive = async (driveId) => {

  try {

    const token = localStorage.getItem('token')

    await axios.put(
      `http://127.0.0.1:5000/api/admin/drive/approve/${driveId}`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    fetchDashboard()

  } catch (error) {

    console.log(error)
  }
}

const rejectDrive = async (driveId) => {

  try {

    const token = localStorage.getItem('token')

    await axios.put(
      `http://127.0.0.1:5000/api/admin/drive/reject/${driveId}`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    fetchDashboard()

  } catch (error) {

    console.log(error)
  }
}

const logout = () => {

  localStorage.removeItem('token')

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
  width: 270px;
  background: #0f172a;
  color: white;
  padding: 25px 18px;

  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.brand h2 {
  font-weight: 700;
}

.brand p {
  color: #cbd5e1;
  font-size: 14px;
}

.menu {
  list-style: none;
  padding: 0;
  margin-top: 40px;
}

.menu li {
  padding: 14px 16px;
  margin-bottom: 12px;
  border-radius: 12px;

  cursor: pointer;

  display: flex;
  align-items: center;
  gap: 12px;

  transition: 0.3s;
}

.menu li:hover,
.menu li.active {
  background: #1e293b;
}

.logout-btn {
  border: none;
  background: #dc2626;
  color: white;
  padding: 12px;
  border-radius: 12px;
  font-weight: 600;
}

/* Main */
.main-content {
  flex: 1;
  padding: 30px;
}

/* Navbar */
.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;

  margin-bottom: 30px;

  flex-wrap: wrap;
  gap: 15px;
}

.search-box input {
  border: none;
  padding: 12px 16px;
  border-radius: 12px;
  width: 280px;
}

/* Stats */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;

  margin-bottom: 25px;
}

.stat-card {
  background: white;
  border-radius: 18px;
  padding: 25px;

  box-shadow: 0 4px 15px rgba(0,0,0,0.06);
}

.stat-card h5 {
  color: #64748b;
}

.stat-card h2 {
  margin-top: 12px;
  font-weight: 700;
}

/* Sections */
.section-card {
  background: white;
  border-radius: 18px;
  padding: 25px;

  box-shadow: 0 4px 15px rgba(0,0,0,0.06);
}

.section-header {
  margin-bottom: 25px;
}

/* Empty */
.empty-box {
  text-align: center;
  padding: 60px 20px;
  color: #64748b;
}

.empty-box i {
  font-size: 60px;
  margin-bottom: 15px;
}

/* Table */
.custom-table thead {
  background: #0f172a;
  color: white;
}

.custom-table {
  border-radius: 12px;
  overflow: hidden;
}

/* Buttons */
.approve-btn,
.reject-btn {
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  margin-right: 8px;
}

.approve-btn {
  background: #16a34a;
}

.reject-btn {
  background: #dc2626;
}

/* Status */
.status-badge {
  padding: 6px 14px;
  border-radius: 30px;
  font-size: 13px;
  font-weight: 600;
}

.pending {
  background: #fef3c7;
  color: #92400e;
}

.approved {
  background: #dcfce7;
  color: #166534;
}

.rejected {
  background: #fee2e2;
  color: #991b1b;
}

/* Loading */
.loading-box {
  background: white;
  border-radius: 18px;
  padding: 80px;
  text-align: center;
  font-size: 20px;
  font-weight: 600;
}

/* Responsive */
@media (max-width: 992px) {

  .admin-dashboard {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
  }

  .main-content {
    padding: 20px;
  }
}

@media (max-width: 576px) {

  .topbar {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-box input {
    width: 100%;
  }
}
</style>