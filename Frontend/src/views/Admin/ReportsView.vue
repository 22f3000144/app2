<template>
  <div class="reports-page">

    <!-- Header -->
    <div class="page-header">

      <div>
        <h2>Placement Reports & Analytics</h2>
        <p>
          Monitor placement activities and statistics
        </p>
      </div>

      <button
        class="export-btn"
        @click="exportReport"
      >
        <i class="bi bi-download"></i>
        Export Report
      </button>

    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading-box">
      Loading Reports...
    </div>

    <!-- Content -->
    <div v-else>

      <!-- Stats -->
      <div class="stats-grid">

        <div class="stat-card">
          <div>
            <h5>Total Students</h5>
            <h2>{{ report.total_students }}</h2>
          </div>

          <i class="bi bi-people-fill"></i>
        </div>

        <div class="stat-card">
          <div>
            <h5>Total Companies</h5>
            <h2>{{ report.total_companies }}</h2>
          </div>

          <i class="bi bi-buildings-fill"></i>
        </div>

        <div class="stat-card">
          <div>
            <h5>Total Drives</h5>
            <h2>{{ report.total_drives }}</h2>
          </div>

          <i class="bi bi-briefcase-fill"></i>
        </div>

        <div class="stat-card">
          <div>
            <h5>Total Applications</h5>
            <h2>{{ report.total_applications }}</h2>
          </div>

          <i class="bi bi-file-earmark-text-fill"></i>
        </div>

      </div>

      <!-- Placement Stats -->
      <div class="analytics-grid">

        <!-- Placement Ratio -->
        <div class="analytics-card">

          <div class="card-header">
            <h4>Placement Ratio</h4>
          </div>

          <div class="ratio-container">

            <div class="circle-progress">

              <svg width="180" height="180">

                <circle
                  cx="90"
                  cy="90"
                  r="70"
                  stroke="#e2e8f0"
                  stroke-width="12"
                  fill="none"
                />

                <circle
                  cx="90"
                  cy="90"
                  r="70"
                  stroke="#2563eb"
                  stroke-width="12"
                  fill="none"
                  stroke-linecap="round"
                  :stroke-dasharray="440"
                  :stroke-dashoffset="progressOffset"
                  transform="rotate(-90 90 90)"
                />

              </svg>

              <div class="progress-text">
                <h2>{{ placementRatio }}%</h2>
                <p>Placed</p>
              </div>

            </div>

          </div>

        </div>

        <!-- Status Summary -->
        <div class="analytics-card">

          <div class="card-header">
            <h4>Application Status Summary</h4>
          </div>

          <div class="status-summary">

            <div class="summary-item">

              <div class="summary-dot applied-dot"></div>

              <div>
                <h5>Applied</h5>
                <p>{{ report.applied }}</p>
              </div>

            </div>

            <div class="summary-item">

              <div class="summary-dot shortlisted-dot"></div>

              <div>
                <h5>Shortlisted</h5>
                <p>{{ report.shortlisted }}</p>
              </div>

            </div>

            <div class="summary-item">

              <div class="summary-dot selected-dot"></div>

              <div>
                <h5>Selected</h5>
                <p>{{ report.selected }}</p>
              </div>

            </div>

            <div class="summary-item">

              <div class="summary-dot rejected-dot"></div>

              <div>
                <h5>Rejected</h5>
                <p>{{ report.rejected }}</p>
              </div>

            </div>

          </div>

        </div>

      </div>

      <!-- Top Companies -->
      <div class="section-card">

        <div class="section-header">
          <h4>Top Hiring Companies</h4>
        </div>

        <div
          v-if="topCompanies.length === 0"
          class="empty-box"
        >
          <i class="bi bi-buildings"></i>

          <h5>No Company Data Found</h5>
        </div>

        <div
          v-else
          class="table-responsive"
        >

          <table class="table report-table">

            <thead>
              <tr>
                <th>Company</th>
                <th>Total Drives</th>
                <th>Total Hires</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>

              <tr
                v-for="company in topCompanies"
                :key="company.id"
              >

                <td>

                  <div class="company-info">

                    <div class="company-logo">
                      {{ company.company_name?.charAt(0) }}
                    </div>

                    <div>
                      <h6>{{ company.company_name }}</h6>

                      <small>
                        Hiring Partner
                      </small>
                    </div>

                  </div>

                </td>

                <td>{{ company.total_drives }}</td>

                <td>{{ company.total_hires }}</td>

                <td>

                  <span
                    class="status-badge approved"
                  >
                    Active
                  </span>

                </td>

              </tr>

            </tbody>

          </table>

        </div>

      </div>

      <!-- Recent Activities -->
      <div class="section-card">

        <div class="section-header">
          <h4>Recent Placement Activities</h4>
        </div>

        <div
          v-if="activities.length === 0"
          class="empty-box"
        >
          <i class="bi bi-clock-history"></i>

          <h5>No Recent Activities</h5>
        </div>

        <div
          v-else
          class="activity-timeline"
        >

          <div
            class="timeline-item"
            v-for="activity in activities"
            :key="activity.id"
          >

            <div class="timeline-dot"></div>

            <div class="timeline-content">

              <h6>{{ activity.title }}</h6>

              <p>{{ activity.description }}</p>

              <small>{{ activity.date }}</small>

            </div>

          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import axios from 'axios'
import { computed, onMounted, ref } from 'vue'

const loading = ref(true)

const report = ref({
  total_students: 0,
  total_companies: 0,
  total_drives: 0,
  total_applications: 0,
  applied: 0,
  shortlisted: 0,
  selected: 0,
  rejected: 0,
})

const topCompanies = ref([])

const activities = ref([])

const fetchReports = async () => {

  try {

    const token = localStorage.getItem('token')

    // Reports
    const reportResponse = await axios.get(
      'http://127.0.0.1:5000/api/admin/reports',
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    report.value = reportResponse.data || {}

    // Top Companies
    const companiesResponse = await axios.get(
      'http://127.0.0.1:5000/api/admin/top-companies',
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    topCompanies.value = companiesResponse.data || []

    // Activities
    const activitiesResponse = await axios.get(
      'http://127.0.0.1:5000/api/admin/activities',
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    activities.value = activitiesResponse.data || []

  } catch (error) {

    console.log(error)

  } finally {

    loading.value = false
  }
}

onMounted(() => {
  fetchReports()
})

const placementRatio = computed(() => {

  if (!report.value.total_students) return 0

  return Math.round(
    (
      report.value.selected /
      report.value.total_students
    ) * 100
  )
})

const progressOffset = computed(() => {

  return 440 - (
    (440 * placementRatio.value) / 100
  )
})

const exportReport = async () => {

  try {

    const token = localStorage.getItem('token')

    const response = await axios.get(
      'http://127.0.0.1:5000/api/admin/export-report',
      {
        responseType: 'blob',

        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    const url = window.URL.createObjectURL(
      new Blob([response.data])
    )

    const link = document.createElement('a')

    link.href = url

    link.setAttribute(
      'download',
      'placement_report.csv'
    )

    document.body.appendChild(link)

    link.click()

  } catch (error) {

    console.log(error)

    alert('Export Failed')
  }
}
</script>

<style scoped>
.reports-page {
  min-height: 100vh;
  background: #f1f5f9;
  padding: 25px;
}

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  gap: 20px;
  flex-wrap: wrap;

  margin-bottom: 30px;
}

.page-header h2 {
  font-weight: 700;
  margin-bottom: 5px;
}

.page-header p {
  color: #64748b;
}

/* Export */
.export-btn {
  border: none;

  background: #2563eb;
  color: white;

  padding: 12px 18px;

  border-radius: 12px;

  font-weight: 600;

  display: flex;
  align-items: center;
  gap: 10px;
}

/* Stats */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));

  gap: 20px;

  margin-bottom: 30px;
}

.stat-card {
  background: white;

  border-radius: 18px;

  padding: 25px;

  display: flex;
  justify-content: space-between;
  align-items: center;

  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.stat-card h5 {
  color: #64748b;
}

.stat-card h2 {
  margin-top: 10px;
  font-weight: 700;
}

.stat-card i {
  font-size: 35px;
  color: #2563eb;
}

/* Analytics */
.analytics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));

  gap: 20px;

  margin-bottom: 30px;
}

.analytics-card {
  background: white;

  border-radius: 18px;

  padding: 25px;

  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.card-header {
  margin-bottom: 25px;
}

/* Progress */
.ratio-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.circle-progress {
  position: relative;
}

.progress-text {
  position: absolute;

  inset: 0;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.progress-text h2 {
  font-weight: 700;
}

/* Status */
.status-summary {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 14px;
}

.summary-dot {
  width: 15px;
  height: 15px;

  border-radius: 50%;
}

.applied-dot {
  background: #facc15;
}

.shortlisted-dot {
  background: #3b82f6;
}

.selected-dot {
  background: #22c55e;
}

.rejected-dot {
  background: #ef4444;
}

/* Section */
.section-card {
  background: white;

  border-radius: 18px;

  padding: 25px;

  margin-bottom: 30px;

  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.section-header {
  margin-bottom: 25px;
}

/* Table */
.report-table thead {
  background: #0f172a;
  color: white;
}

.report-table th,
.report-table td {
  vertical-align: middle;
  padding: 16px;
}

/* Company */
.company-info {
  display: flex;
  align-items: center;
  gap: 14px;
}

.company-logo {
  width: 45px;
  height: 45px;

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

.approved {
  background: #dcfce7;
  color: #166534;
}

/* Activity */
.activity-timeline {
  position: relative;
  padding-left: 20px;
}

.timeline-item {
  position: relative;
  margin-bottom: 25px;
}

.timeline-dot {
  width: 14px;
  height: 14px;

  background: #2563eb;

  border-radius: 50%;

  position: absolute;

  left: -27px;
  top: 5px;
}

.timeline-content {
  background: #f8fafc;

  border-radius: 14px;

  padding: 18px;
}

.timeline-content h6 {
  font-weight: 600;
  margin-bottom: 8px;
}

.timeline-content p {
  color: #64748b;
  margin-bottom: 8px;
}

.timeline-content small {
  color: #94a3b8;
}

/* Empty */
.empty-box {
  text-align: center;

  padding: 80px 20px;

  color: #64748b;
}

.empty-box i {
  font-size: 60px;
  margin-bottom: 15px;
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

  .report-table {
    min-width: 900px;
  }
}

@media (max-width: 576px) {

  .reports-page {
    padding: 15px;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .export-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>