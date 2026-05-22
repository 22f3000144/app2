<template>
  <div class="dashboard-wrapper">

    <!-- Sidebar -->
    <aside class="sidebar">

      <div>
        <div class="brand">
          <h2>Eduvora</h2>
          <p>Student Dashboard</p>
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
            :class="{ active: activeMenu === 'jobs' }"
            @click="activeMenu = 'jobs'"
          >
            <i class="bi bi-briefcase-fill"></i>
            Jobs
          </li>

          <li
            :class="{ active: activeMenu === 'applications' }"
            @click="activeMenu = 'applications'"
          >
            <i class="bi bi-file-earmark-text-fill"></i>
            Applications
          </li>

          <li
            :class="{ active: activeMenu === 'profile' }"
            @click="activeMenu = 'profile'"
          >
            <i class="bi bi-person-circle"></i>
            Profile
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
          <h3>Welcome, {{ student.name || route.params.name }}</h3>
          <p>Placement Portal Student Panel</p>
        </div>

        <div class="search-box">
          <input
            type="text"
            placeholder="Search jobs..."
            v-model="search"
          />
        </div>

      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-box">
        Loading Dashboard...
      </div>

      <!-- Dashboard -->
      <div v-else>

        <!-- Dashboard Section -->
        <section v-if="activeMenu === 'dashboard'">

          <div class="stats-grid">

            <div class="stat-card">
              <h5>Total Jobs</h5>
              <h2>{{ jobs.length }}</h2>
            </div>

            <div class="stat-card">
              <h5>Applications</h5>
              <h2>{{ applications.length }}</h2>
            </div>

            <div class="stat-card">
              <h5>Selected</h5>
              <h2>{{ selectedCount }}</h2>
            </div>

            <div class="stat-card">
              <h5>Rejected</h5>
              <h2>{{ rejectedCount }}</h2>
            </div>

          </div>

          <!-- Latest Jobs -->
          <div class="section-card">

            <div class="section-header">
              <h4>Latest Placement Drives</h4>
            </div>

            <!-- No Jobs -->
            <div
              v-if="filteredJobs.length === 0"
              class="empty-box"
            >
              <i class="bi bi-briefcase"></i>
              <h5>No Placement Drives Available</h5>
              <p>
                Approved placement drives will appear here.
              </p>
            </div>

            <!-- Jobs -->
            <div v-else class="job-grid">

              <div
                class="job-card"
                v-for="job in filteredJobs"
                :key="job.id"
              >

                <div class="job-top">
                  <h5>{{ job.job_title }}</h5>
                  <span>{{ job.company_name }}</span>
                </div>

                <p class="job-description">
                  {{ job.job_description }}
                </p>

                <div class="job-details">
                  <p><strong>Branch:</strong> {{ job.branch }}</p>
                  <p><strong>CGPA:</strong> {{ job.cgpa }}</p>
                  <p><strong>Deadline:</strong> {{ job.deadline }}</p>
                </div>

                <button
                  class="apply-btn"
                  @click="applyJob(job.id)"
                >
                  Apply Now
                </button>

              </div>

            </div>

          </div>

        </section>

        <!-- Jobs Section -->
        <section v-if="activeMenu === 'jobs'">

          <div class="section-card">

            <div class="section-header">
              <h4>All Placement Drives</h4>
            </div>

            <div
              v-if="filteredJobs.length === 0"
              class="empty-box"
            >
              <i class="bi bi-search"></i>
              <h5>No Jobs Found</h5>
            </div>

            <div v-else class="table-responsive">

              <table class="table custom-table">

                <thead>
                  <tr>
                    <th>Company</th>
                    <th>Role</th>
                    <th>Branch</th>
                    <th>Deadline</th>
                    <th>Action</th>
                  </tr>
                </thead>

                <tbody>

                  <tr
                    v-for="job in filteredJobs"
                    :key="job.id"
                  >
                    <td>{{ job.company_name }}</td>
                    <td>{{ job.job_title }}</td>
                    <td>{{ job.branch }}</td>
                    <td>{{ job.deadline }}</td>

                    <td>
                      <button
                        class="table-btn"
                        @click="applyJob(job.id)"
                      >
                        Apply
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
              <h4>My Applications</h4>
            </div>

            <!-- No Applications -->
            <div
              v-if="applications.length === 0"
              class="empty-box"
            >
              <i class="bi bi-file-earmark-x"></i>
              <h5>No Applications Yet</h5>

              <p>
                Once you apply for jobs, they will appear here.
              </p>
            </div>

            <!-- Applications Table -->
            <div v-else class="table-responsive">

              <table class="table custom-table">

                <thead>
                  <tr>
                    <th>Company</th>
                    <th>Role</th>
                    <th>Status</th>
                    <th>Applied Date</th>
                  </tr>
                </thead>

                <tbody>

                  <tr
                    v-for="application in applications"
                    :key="application.id"
                  >

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

                    <td>{{ application.applied_date }}</td>

                  </tr>

                </tbody>

              </table>

            </div>

          </div>

        </section>

        <!-- Profile -->
        <section v-if="activeMenu === 'profile'">

          <div class="section-card">

            <div class="section-header">
              <h4>Student Profile</h4>
            </div>

            <form class="profile-form">

              <div class="row">

                <div class="col-md-6 mb-3">
                  <label>Name</label>

                  <input
                    type="text"
                    class="form-control"
                    v-model="student.name"
                  />
                </div>

                <div class="col-md-6 mb-3">
                  <label>Email</label>

                  <input
                    type="email"
                    class="form-control"
                    v-model="student.email"
                  />
                </div>

                <div class="col-md-6 mb-3">
                  <label>Branch</label>

                  <input
                    type="text"
                    class="form-control"
                    v-model="student.branch"
                  />
                </div>

                <div class="col-md-6 mb-3">
                  <label>CGPA</label>

                  <input
                    type="text"
                    class="form-control"
                    v-model="student.cgpa"
                  />
                </div>

                <div class="col-md-6 mb-3">
                  <label>Graduation Year</label>

                  <input
                    type="text"
                    class="form-control"
                    v-model="student.year"
                  />
                </div>

                <div class="col-md-6 mb-3">
                  <label>Resume</label>

                  <input
                    type="file"
                    class="form-control"
                  />
                </div>

              </div>

              <button
                type="button"
                class="save-btn"
              >
                Save Profile
              </button>

            </form>

          </div>

        </section>

      </div>

    </main>

  </div>
</template>

<script setup>
import axios from 'axios'
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()

const loading = ref(true)

const activeMenu = ref('dashboard')

const search = ref('')

const student = ref({})

const jobs = ref([])

const applications = ref([])

const fetchDashboard = async () => {

  try {

    const token = localStorage.getItem('token')

    // Student Data
    const studentResponse = await axios.get(
      'http://127.0.0.1:5000/api/student/profile',
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    student.value = studentResponse.data

    // Approved Jobs
    const jobsResponse = await axios.get(
      'http://127.0.0.1:5000/api/student/drives',
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    jobs.value = jobsResponse.data || []

    // Applications
    const applicationsResponse = await axios.get(
      'http://127.0.0.1:5000/api/student/applications',
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

const filteredJobs = computed(() => {

  return jobs.value.filter((job) => {

    return (
      job.job_title
        ?.toLowerCase()
        .includes(search.value.toLowerCase()) ||

      job.company_name
        ?.toLowerCase()
        .includes(search.value.toLowerCase())
    )
  })
})

const selectedCount = computed(() => {

  return applications.value.filter(
    (application) =>
      application.status === 'Selected'
  ).length
})

const rejectedCount = computed(() => {

  return applications.value.filter(
    (application) =>
      application.status === 'Rejected'
  ).length
})

const applyJob = async (driveId) => {

  try {

    const token = localStorage.getItem('token')

    await axios.post(
      `http://127.0.0.1:5000/api/student/apply/${driveId}`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    alert('Applied Successfully')

    fetchDashboard()

  } catch (error) {

    console.log(error)

    if (error.response?.status === 409) {

      alert('Already Applied')

    } else {

      alert('Application Failed')
    }
  }
}

const logout = () => {

  localStorage.removeItem('token')

  router.push('/login')
}
</script>

<style scoped>
.dashboard-wrapper {
  display: flex;
  min-height: 100vh;
  background: #f4f7fb;
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
  margin-bottom: 4px;
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
  transition: 0.3s;
  display: flex;
  align-items: center;
  gap: 12px;
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
  width: 280px;
  border-radius: 12px;
  background: white;
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

/* Jobs */
.job-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
  gap: 20px;
}

.job-card {
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 20px;
  transition: 0.3s;
}

.job-card:hover {
  transform: translateY(-4px);
}

.job-top {
  margin-bottom: 10px;
}

.job-top span {
  color: #2563eb;
  font-weight: 600;
}

.job-description {
  color: #64748b;
  margin-bottom: 15px;
}

.job-details p {
  margin-bottom: 6px;
}

.apply-btn,
.table-btn,
.save-btn {
  border: none;
  background: #2563eb;
  color: white;
  padding: 11px 18px;
  border-radius: 10px;
  font-weight: 600;
  margin-top: 15px;
}

.save-btn {
  background: #16a34a;
}

.table-btn {
  margin-top: 0;
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

/* Status */
.status-badge {
  padding: 6px 14px;
  border-radius: 30px;
  font-size: 13px;
  font-weight: 600;
}

.applied {
  background: #fef3c7;
  color: #92400e;
}

.shortlisted {
  background: #dbeafe;
  color: #1d4ed8;
}

.selected {
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
  padding: 80px;
  border-radius: 18px;
  text-align: center;
  font-size: 20px;
  font-weight: 600;
}

/* Responsive */
@media (max-width: 992px) {

  .dashboard-wrapper {
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

  .job-grid {
    grid-template-columns: 1fr;
  }
}
</style>