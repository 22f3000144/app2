<template>
  <div class="admin-home">

    <!-- Stats -->
    <div class="stats-grid">

      <div class="stat-card students">

        <div>

          <h5>Total Students</h5>

          <h2>{{ dashboard.total_students }}</h2>

          <p>
            Registered Students
          </p>

        </div>

        <div class="stat-icon">
          <i class="bi bi-people-fill"></i>
        </div>

      </div>

      <div class="stat-card companies">

        <div>

          <h5>Total Companies</h5>

          <h2>{{ dashboard.total_companies }}</h2>

          <p>
            Hiring Companies
          </p>

        </div>

        <div class="stat-icon">
          <i class="bi bi-buildings-fill"></i>
        </div>

      </div>

      <div class="stat-card drives">

        <div>

          <h5>Total Drives</h5>

          <h2>{{ dashboard.total_drives }}</h2>

          <p>
            Placement Drives
          </p>

        </div>

        <div class="stat-icon">
          <i class="bi bi-briefcase-fill"></i>
        </div>

      </div>

      <div class="stat-card applications">

        <div>

          <h5>Total Applications</h5>

          <h2>{{ dashboard.total_applications }}</h2>

          <p>
            Submitted Applications
          </p>

        </div>

        <div class="stat-icon">
          <i class="bi bi-file-earmark-text-fill"></i>
        </div>

      </div>

    </div>

    <!-- Grid -->
    <div class="dashboard-grid">

      <!-- Recent Drives -->
      <div class="dashboard-card">

        <div class="card-header">

          <h4>Recent Placement Drives</h4>

          <RouterLink
            to="/admin/drives"
            class="view-link"
          >
            View All
          </RouterLink>

        </div>

        <div
          v-if="recentDrives.length === 0"
          class="empty-box"
        >

          <i class="bi bi-briefcase"></i>

          <h5>No Placement Drives</h5>

        </div>

        <div
          v-else
          class="table-responsive"
        >

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
                v-for="drive in recentDrives"
                :key="drive.id"
              >

                <td>

                  <div class="company-info">

                    <div class="company-logo">
                      {{ drive.company_name?.charAt(0) }}
                    </div>

                    <span>
                      {{ drive.company_name }}
                    </span>

                  </div>

                </td>

                <td>{{ drive.job_title }}</td>

                <td>

                  <span
                    class="status-badge"
                    :class="drive.status?.toLowerCase()"
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

      <!-- Quick Analytics -->
      <div class="dashboard-card">

        <div class="card-header">
          <h4>Quick Analytics</h4>
        </div>

        <div class="analytics-list">

          <div class="analytics-item">

            <div class="analytics-info">

              <h6>Approved Companies</h6>

              <p>
                {{ dashboard.approved_companies }}
              </p>

            </div>

            <div class="analytics-circle green">
              <i class="bi bi-check-circle-fill"></i>
            </div>

          </div>

          <div class="analytics-item">

            <div class="analytics-info">

              <h6>Pending Drives</h6>

              <p>
                {{ dashboard.pending_drives }}
              </p>

            </div>

            <div class="analytics-circle yellow">
              <i class="bi bi-hourglass-split"></i>
            </div>

          </div>

          <div class="analytics-item">

            <div class="analytics-info">

              <h6>Selected Students</h6>

              <p>
                {{ dashboard.selected_students }}
              </p>

            </div>

            <div class="analytics-circle blue">
              <i class="bi bi-award-fill"></i>
            </div>

          </div>

          <div class="analytics-item">

            <div class="analytics-info">

              <h6>Rejected Applications</h6>

              <p>
                {{ dashboard.rejected_applications }}
              </p>

            </div>

            <div class="analytics-circle red">
              <i class="bi bi-x-circle-fill"></i>
            </div>

          </div>

        </div>

      </div>

    </div>

    <!-- Recent Applications -->
    <div class="dashboard-card">

      <div class="card-header">

        <h4>Recent Applications</h4>

        <RouterLink
          to="/admin/reports"
          class="view-link"
        >
          View Reports
        </RouterLink>

      </div>

      <div
        v-if="recentApplications.length === 0"
        class="empty-box"
      >

        <i class="bi bi-file-earmark"></i>

        <h5>No Applications Found</h5>

      </div>

      <div
        v-else
        class="table-responsive"
      >

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
              v-for="application in recentApplications"
              :key="application.id"
            >

              <td>{{ application.student_name }}</td>

              <td>{{ application.company_name }}</td>

              <td>{{ application.job_title }}</td>

              <td>

                <span
                  class="status-badge"
                  :class="application.status?.toLowerCase()"
                >
                  {{ application.status }}
                </span>

              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

  </div>
</template>

<script setup>
import axios from 'axios'

import {
  onMounted,
  ref,
} from 'vue'

import { RouterLink } from 'vue-router'

const dashboard = ref({
  total_students: 0,
  total_companies: 0,
  total_drives: 0,
  total_applications: 0,
  approved_companies: 0,
  pending_drives: 0,
  selected_students: 0,
  rejected_applications: 0,
})

const recentDrives = ref([])

const recentApplications = ref([])

const fetchDashboard = async () => {

  try {

    const token = localStorage.getItem('token')

    // Dashboard Stats
    const dashboardResponse = await axios.get(
      'http://127.0.0.1:5000/api/admin/dashboard',
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    dashboard.value = dashboardResponse.data || {}

    // Drives
    const drivesResponse = await axios.get(
      'http://127.0.0.1:5000/api/admin/drives',
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    recentDrives.value =
      drivesResponse.data?.slice(0, 5) || []

    // Applications
    const applicationsResponse = await axios.get(
      'http://127.0.0.1:5000/api/admin/applications',
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    recentApplications.value =
      applicationsResponse.data?.slice(0, 5) || []

  } catch (error) {

    console.log(error)
  }
}

onMounted(() => {
  fetchDashboard()
})
</script>

<style scoped>
.admin-home {
  width: 100%;
}

/* Stats */
.stats-grid {
  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(230px, 1fr));

  gap: 22px;

  margin-bottom: 25px;
}

.stat-card {
  background: white;

  border-radius: 22px;

  padding: 25px;

  display: flex;
  justify-content: space-between;
  align-items: center;

  box-shadow: 0 4px 15px rgba(0,0,0,0.05);

  transition: 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-card h5 {
  color: #64748b;
  margin-bottom: 10px;
}

.stat-card h2 {
  font-size: 34px;
  font-weight: 700;
}

.stat-card p {
  color: #94a3b8;
  margin-top: 8px;
}

.stat-icon {
  width: 68px;
  height: 68px;

  border-radius: 18px;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 28px;

  color: white;
}

/* Card Colors */
.students .stat-icon {
  background: #2563eb;
}

.companies .stat-icon {
  background: #16a34a;
}

.drives .stat-icon {
  background: #ea580c;
}

.applications .stat-icon {
  background: #7c3aed;
}

/* Dashboard Grid */
.dashboard-grid {
  display: grid;

  grid-template-columns: 2fr 1fr;

  gap: 22px;

  margin-bottom: 25px;
}

/* Dashboard Card */
.dashboard-card {
  background: white;

  border-radius: 22px;

  padding: 24px;

  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

/* Header */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  margin-bottom: 22px;
}

.card-header h4 {
  font-weight: 700;
}

.view-link {
  text-decoration: none;

  color: #2563eb;

  font-weight: 600;
}

/* Table */
.custom-table thead {
  background: #0f172a;
  color: white;
}

.custom-table {
  border-radius: 14px;
  overflow: hidden;
}

.custom-table th,
.custom-table td {
  vertical-align: middle;
  padding: 16px;
}

/* Company */
.company-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.company-logo {
  width: 40px;
  height: 40px;

  border-radius: 50%;

  background: #2563eb;
  color: white;

  display: flex;
  align-items: center;
  justify-content: center;

  font-weight: 700;
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

.closed {
  background: #dbeafe;
  color: #1d4ed8;
}

/* Analytics */
.analytics-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.analytics-item {
  background: #f8fafc;

  border-radius: 16px;

  padding: 16px;

  display: flex;
  justify-content: space-between;
  align-items: center;
}

.analytics-info h6 {
  margin-bottom: 6px;
  font-weight: 600;
}

.analytics-info p {
  margin: 0;

  font-size: 22px;
  font-weight: 700;
}

.analytics-circle {
  width: 52px;
  height: 52px;

  border-radius: 14px;

  display: flex;
  align-items: center;
  justify-content: center;

  color: white;

  font-size: 22px;
}

.green {
  background: #16a34a;
}

.yellow {
  background: #f59e0b;
}

.blue {
  background: #2563eb;
}

.red {
  background: #dc2626;
}

/* Empty */
.empty-box {
  text-align: center;

  padding: 60px 20px;

  color: #64748b;
}

.empty-box i {
  font-size: 55px;
  margin-bottom: 15px;
}

/* Responsive */
@media (max-width: 1200px) {

  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 992px) {

  .custom-table {
    min-width: 700px;
  }
}

@media (max-width: 576px) {

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .dashboard-card {
    padding: 18px;
  }

  .stat-card {
    padding: 20px;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style>