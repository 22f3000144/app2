<template>
  <div class="manage-drives-page">

    <!-- Header -->
    <div class="page-header">

      <div>
        <h2>Manage Placement Drives</h2>
        <p>
          Approve, reject and manage placement drives
        </p>
      </div>

      <div class="search-box">
        <input
          type="text"
          placeholder="Search drives..."
          v-model="search"
        />
      </div>

    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading-box">
      Loading Placement Drives...
    </div>

    <!-- Content -->
    <div v-else>

      <!-- Empty -->
      <div
        v-if="filteredDrives.length === 0"
        class="empty-box"
      >

        <i class="bi bi-briefcase"></i>

        <h4>No Placement Drives Found</h4>

        <p>
          Company placement drives will appear here.
        </p>

      </div>

      <!-- Drives -->
      <div
        v-else
        class="table-responsive drives-table-wrapper"
      >

        <table class="table drives-table">

          <thead>
            <tr>
              <th>ID</th>
              <th>Company</th>
              <th>Job Title</th>
              <th>Branch</th>
              <th>CGPA</th>
              <th>Deadline</th>
              <th>Status</th>
              <th>Applications</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="drive in filteredDrives"
              :key="drive.id"
            >

              <td>{{ drive.id }}</td>

              <!-- Company -->
              <td>

                <div class="company-info">

                  <div class="company-logo">
                    {{ drive.company_name?.charAt(0) }}
                  </div>

                  <div>

                    <h6>{{ drive.company_name }}</h6>

                    <small>
                      Registered Company
                    </small>

                  </div>

                </div>

              </td>

              <!-- Job Title -->
              <td>

                <div class="job-info">

                  <h6>{{ drive.job_title }}</h6>

                  <small>
                    {{ drive.job_description }}
                  </small>

                </div>

              </td>

              <!-- Eligibility -->
              <td>{{ drive.branch }}</td>

              <td>{{ drive.cgpa }}</td>

              <!-- Deadline -->
              <td>{{ drive.deadline }}</td>

              <!-- Status -->
              <td>

                <span
                  class="status-badge"
                  :class="drive.status?.toLowerCase()"
                >
                  {{ drive.status }}
                </span>

              </td>

              <!-- Applications -->
              <td>

                <span class="application-count">
                  {{ drive.total_applications || 0 }}
                </span>

              </td>

              <!-- Actions -->
              <td>

                <div class="action-buttons">

                  <button
                    class="view-btn"
                    @click="viewDrive(drive)"
                  >
                    View
                  </button>

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

                  <button
                    class="delete-btn"
                    @click="deleteDrive(drive.id)"
                  >
                    Delete
                  </button>

                </div>

              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

    <!-- View Modal -->
    <div
      v-if="selectedDrive"
      class="modal-overlay"
    >

      <div class="drive-modal">

        <div class="modal-header">

          <h4>Drive Details</h4>

          <button
            class="close-btn"
            @click="selectedDrive = null"
          >
            ×
          </button>

        </div>

        <div class="modal-body">

          <div class="company-circle">
            {{ selectedDrive.company_name?.charAt(0) }}
          </div>

          <h3>{{ selectedDrive.job_title }}</h3>

          <p class="company-name">
            {{ selectedDrive.company_name }}
          </p>

          <div class="details-grid">

            <div class="detail-card">
              <h6>Branch</h6>
              <p>{{ selectedDrive.branch }}</p>
            </div>

            <div class="detail-card">
              <h6>CGPA</h6>
              <p>{{ selectedDrive.cgpa }}</p>
            </div>

            <div class="detail-card">
              <h6>Deadline</h6>
              <p>{{ selectedDrive.deadline }}</p>
            </div>

            <div class="detail-card">
              <h6>Status</h6>
              <p>{{ selectedDrive.status }}</p>
            </div>

          </div>

          <div class="description-box">

            <h5>Job Description</h5>

            <p>
              {{ selectedDrive.job_description }}
            </p>

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

const search = ref('')

const drives = ref([])

const selectedDrive = ref(null)

const fetchDrives = async () => {

  try {

    const token = localStorage.getItem('token')

    const response = await axios.get(
      'http://127.0.0.1:5000/api/admin/drives',
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    drives.value = response.data || []

  } catch (error) {

    console.log(error)

  } finally {

    loading.value = false
  }
}

onMounted(() => {
  fetchDrives()
})

const filteredDrives = computed(() => {

  return drives.value.filter((drive) => {

    return (

      drive.company_name
        ?.toLowerCase()
        .includes(search.value.toLowerCase()) ||

      drive.job_title
        ?.toLowerCase()
        .includes(search.value.toLowerCase()) ||

      drive.branch
        ?.toLowerCase()
        .includes(search.value.toLowerCase())
    )
  })
})

const viewDrive = (drive) => {

  selectedDrive.value = drive
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

    alert('Drive Approved')

    fetchDrives()

  } catch (error) {

    console.log(error)

    alert('Approval Failed')
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

    alert('Drive Rejected')

    fetchDrives()

  } catch (error) {

    console.log(error)

    alert('Reject Failed')
  }
}

const deleteDrive = async (driveId) => {

  const confirmDelete = confirm(
    'Are you sure you want to delete this drive?'
  )

  if (!confirmDelete) return

  try {

    const token = localStorage.getItem('token')

    await axios.delete(
      `http://127.0.0.1:5000/api/admin/drive/${driveId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    alert('Drive Deleted')

    fetchDrives()

  } catch (error) {

    console.log(error)

    alert('Delete Failed')
  }
}
</script>

<style scoped>
.manage-drives-page {
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

/* Search */
.search-box input {
  width: 280px;

  border: none;
  outline: none;

  background: white;

  padding: 12px 16px;

  border-radius: 12px;

  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

/* Table */
.drives-table-wrapper {
  background: white;

  border-radius: 18px;

  padding: 20px;

  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.drives-table {
  margin-bottom: 0;
}

.drives-table thead {
  background: #0f172a;
  color: white;
}

.drives-table th,
.drives-table td {
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
  font-size: 18px;
}

.company-info h6 {
  margin-bottom: 2px;
  font-weight: 600;
}

.company-info small {
  color: #64748b;
}

/* Job */
.job-info h6 {
  margin-bottom: 5px;
  font-weight: 600;
}

.job-info small {
  color: #64748b;
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

/* Application Count */
.application-count {
  background: #2563eb;
  color: white;

  padding: 8px 12px;

  border-radius: 10px;

  font-size: 14px;
  font-weight: 600;
}

/* Buttons */
.action-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.view-btn,
.approve-btn,
.reject-btn,
.delete-btn {
  border: none;

  padding: 8px 14px;

  border-radius: 10px;

  color: white;

  font-size: 14px;
  font-weight: 600;

  transition: 0.3s;
}

.view-btn {
  background: #2563eb;
}

.approve-btn {
  background: #16a34a;
}

.reject-btn {
  background: #ea580c;
}

.delete-btn {
  background: #dc2626;
}

.view-btn:hover,
.approve-btn:hover,
.reject-btn:hover,
.delete-btn:hover {
  transform: translateY(-2px);
}

/* Empty */
.empty-box {
  background: white;

  border-radius: 18px;

  padding: 80px 20px;

  text-align: center;

  color: #64748b;
}

.empty-box i {
  font-size: 65px;
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

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;

  background: rgba(0,0,0,0.4);

  display: flex;
  align-items: center;
  justify-content: center;

  z-index: 1000;
}

.drive-modal {
  width: 100%;
  max-width: 700px;

  background: white;

  border-radius: 20px;

  padding: 25px;

  animation: popup 0.3s ease;
}

@keyframes popup {

  from {
    transform: scale(0.9);
    opacity: 0;
  }

  to {
    transform: scale(1);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  margin-bottom: 25px;
}

.close-btn {
  border: none;
  background: transparent;

  font-size: 28px;

  cursor: pointer;
}

.modal-body {
  text-align: center;
}

.company-circle {
  width: 90px;
  height: 90px;

  border-radius: 50%;

  background: #2563eb;
  color: white;

  margin: auto;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 32px;
  font-weight: 700;

  margin-bottom: 18px;
}

.company-name {
  color: #64748b;
  margin-bottom: 25px;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));

  gap: 18px;

  margin-top: 30px;
}

.detail-card {
  background: #f8fafc;

  border-radius: 14px;

  padding: 18px;
}

.detail-card h6 {
  color: #64748b;
  margin-bottom: 10px;
}

/* Description */
.description-box {
  margin-top: 30px;

  text-align: left;

  background: #f8fafc;

  border-radius: 14px;

  padding: 20px;
}

.description-box h5 {
  margin-bottom: 12px;
}

/* Responsive */
@media (max-width: 992px) {

  .drives-table {
    min-width: 1300px;
  }
}

@media (max-width: 576px) {

  .manage-drives-page {
    padding: 15px;
  }

  .search-box input {
    width: 100%;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .drive-modal {
    margin: 15px;
  }
}
</style>