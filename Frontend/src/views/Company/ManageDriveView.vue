<template>
  <div class="manage-drive-page">

    <div class="container py-5">

      <!-- PAGE HEADER -->

      <div class="page-header mb-4">

        <div>

          <h2>
            Manage Placement Drives
          </h2>

          <p>
            View, update and manage all created placement drives.
          </p>

        </div>

        <router-link
          to="/company/drive/create"
          class="btn btn-primary"
        >

          <i class="bi bi-plus-circle me-2"></i>

          Create Drive

        </router-link>

      </div>

      <!-- ALERT -->

      <div
        v-if="message"
        class="alert"
        :class="success ? 'alert-success' : 'alert-danger'"
      >
        {{ message }}
      </div>

      <!-- LOADING -->

      <div
        v-if="loading"
        class="loading-section"
      >

        <div class="spinner-border text-primary"></div>

        <p class="mt-3">
          Loading placement drives...
        </p>

      </div>

      <!-- EMPTY -->

      <div
        v-else-if="drives.length === 0"
        class="empty-card"
      >

        <i class="bi bi-briefcase"></i>

        <h4>
          No Placement Drives Found
        </h4>

        <p>
          Create your first placement drive to start recruitment.
        </p>

      </div>

      <!-- DRIVE LIST -->

      <div
        v-else
        class="row g-4"
      >

        <div
          class="col-lg-6"
          v-for="drive in drives"
          :key="drive.id"
        >

          <div class="drive-card">

            <!-- HEADER -->

            <div class="drive-top">

              <div>

                <h4>
                  {{ drive.job_title }}
                </h4>

                <span
                  class="status-badge"
                  :class="getStatusClass(drive.status)"
                >
                  {{ drive.status }}
                </span>

              </div>

              <div class="applicant-box">

                <h5>
                  {{ drive.total_applicants }}
                </h5>

                <span>
                  Applicants
                </span>

              </div>

            </div>

            <!-- BODY -->

            <div class="drive-body">

              <p class="description">
                {{ drive.job_description }}
              </p>

              <div class="detail-grid">

                <div class="detail-item">

                  <span class="label">
                    Branch
                  </span>

                  <span class="value">
                    {{ drive.required_branch }}
                  </span>

                </div>

                <div class="detail-item">

                  <span class="label">
                    Minimum CGPA
                  </span>

                  <span class="value">
                    {{ drive.min_cgpa }}
                  </span>

                </div>

                <div class="detail-item">

                  <span class="label">
                    Passing Year
                  </span>

                  <span class="value">
                    {{ drive.passing_year }}
                  </span>

                </div>

                <div class="detail-item">

                  <span class="label">
                    Deadline
                  </span>

                  <span class="value">
                    {{ formatDate(drive.application_deadline) }}
                  </span>

                </div>

              </div>

            </div>

            <!-- FOOTER -->

            <div class="drive-footer">

              <button
                class="btn btn-outline-primary"
                @click="openEditModal(drive)"
              >

                <i class="bi bi-pencil-square me-2"></i>

                Edit

              </button>

              <router-link
                :to="`/company/drive/${drive.id}/applicants`"
                class="btn btn-outline-dark"
              >

                <i class="bi bi-people me-2"></i>

                Applicants

              </router-link>

              <button
                class="btn btn-outline-danger"
                @click="deleteDrive(drive.id)"
              >

                <i class="bi bi-trash me-2"></i>

                Delete

              </button>

            </div>

          </div>

        </div>

      </div>

    </div>

    <!-- EDIT MODAL -->

    <div
      v-if="showModal"
      class="custom-modal"
    >

      <div class="modal-card">

        <div class="modal-header">

          <h4>
            Update Placement Drive
          </h4>

          <button
            class="close-btn"
            @click="closeModal"
          >
            ✕
          </button>

        </div>

        <form @submit.prevent="updateDrive">

          <div class="mb-3">

            <label class="form-label">
              Job Title
            </label>

            <input
              type="text"
              class="form-control"
              v-model="editForm.job_title"
            />

          </div>

          <div class="mb-3">

            <label class="form-label">
              Job Description
            </label>

            <textarea
              rows="5"
              class="form-control"
              v-model="editForm.job_description"
            ></textarea>

          </div>

          <div class="row">

            <div class="col-md-6 mb-3">

              <label class="form-label">
                Required Branch
              </label>

              <input
                type="text"
                class="form-control"
                v-model="editForm.required_branch"
              />

            </div>

            <div class="col-md-6 mb-3">

              <label class="form-label">
                Minimum CGPA
              </label>

              <input
                type="number"
                step="0.1"
                class="form-control"
                v-model="editForm.min_cgpa"
              />

            </div>

            <div class="col-md-6 mb-3">

              <label class="form-label">
                Passing Year
              </label>

              <input
                type="number"
                class="form-control"
                v-model="editForm.passing_year"
              />

            </div>

            <div class="col-md-6 mb-3">

              <label class="form-label">
                Deadline
              </label>

              <input
                type="date"
                class="form-control"
                v-model="editForm.application_deadline"
              />

            </div>

          </div>

          <button
            type="submit"
            class="btn btn-primary w-100 mt-2"
            :disabled="updateLoading"
          >

            <span
              v-if="updateLoading"
              class="spinner-border spinner-border-sm me-2"
            ></span>

            {{ updateLoading ? "Updating..." : "Update Drive" }}

          </button>

        </form>

      </div>

    </div>

  </div>
</template>

<script>
import axios from "axios"

export default {

  name: "ManageDriveView",

  data() {

    return {

      loading: false,

      updateLoading: false,

      success: false,

      message: "",

      drives: [],

      showModal: false,

      editDriveId: null,

      editForm: {

        job_title: "",

        job_description: "",

        required_branch: "",

        min_cgpa: "",

        passing_year: "",

        application_deadline: ""

      }

    }

  },

  mounted() {

    this.fetchDrives()

  },

  methods: {

    async fetchDrives() {

      try {

        this.loading = true

        const token = localStorage.getItem("token")

        const response = await axios.get(

          "http://127.0.0.1:5000/api/company/drives",

          {

            headers: {

              Authorization: `Bearer ${token}`

            }

          }

        )

        this.drives = response.data

      }

      catch (error) {

        this.message =
          "Failed to load placement drives."

      }

      finally {

        this.loading = false

      }

    },

    formatDate(date) {

      return new Date(date).toLocaleDateString()

    },

    getStatusClass(status) {

      if (status === "approved") {

        return "approved"

      }

      else if (status === "pending") {

        return "pending"

      }

      else {

        return "closed"

      }

    },

    openEditModal(drive) {

      this.editDriveId = drive.id

      this.editForm = {

        job_title: drive.job_title,

        job_description: drive.job_description,

        required_branch: drive.required_branch,

        min_cgpa: drive.min_cgpa,

        passing_year: drive.passing_year,

        application_deadline:
          drive.application_deadline

      }

      this.showModal = true

    },

    closeModal() {

      this.showModal = false

    },

    async updateDrive() {

      try {

        this.updateLoading = true

        const token = localStorage.getItem("token")

        const response = await axios.put(

          `http://127.0.0.1:5000/api/company/drive/update/${this.editDriveId}`,

          this.editForm,

          {

            headers: {

              Authorization: `Bearer ${token}`

            }

          }

        )

        this.success = true

        this.message = response.data.message

        this.closeModal()

        this.fetchDrives()

      }

      catch (error) {

        this.success = false

        this.message =
          error.response?.data?.message ||
          "Failed to update drive."

      }

      finally {

        this.updateLoading = false

      }

    },

    async deleteDrive(driveId) {

      const confirmDelete = confirm(
        "Are you sure you want to delete this drive?"
      )

      if (!confirmDelete) {

        return

      }

      try {

        const token = localStorage.getItem("token")

        const response = await axios.delete(

          `http://127.0.0.1:5000/api/company/drive/delete/${driveId}`,

          {

            headers: {

              Authorization: `Bearer ${token}`

            }

          }

        )

        this.success = true

        this.message = response.data.message

        this.fetchDrives()

      }

      catch (error) {

        this.success = false

        this.message =
          error.response?.data?.message ||
          "Failed to delete drive."

      }

    }

  }

}
</script>

<style scoped>

/* =========================
   PAGE
========================= */

.manage-drive-page {
  min-height: 100vh;
  background: #f5f7fb;
}

/* =========================
   HEADER
========================= */

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.page-header h2 {
  font-size: 2.3rem;
  font-weight: 700;
  color: #0f172a;
}

.page-header p {
  color: #64748b;
  margin-top: 10px;
}

/* =========================
   DRIVE CARD
========================= */

.drive-card {
  background: white;
  border-radius: 24px;
  padding: 28px;
  height: 100%;
  box-shadow:
    0 8px 24px rgba(0,0,0,0.05);
  transition: 0.3s ease;
}

.drive-card:hover {
  transform: translateY(-5px);
}

.drive-top {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 25px;
}

.drive-top h4 {
  font-weight: 700;
  margin-bottom: 12px;
  color: #0f172a;
}

.status-badge {
  padding: 8px 14px;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: capitalize;
}

.approved {
  background: #dcfce7;
  color: #15803d;
}

.pending {
  background: #fef3c7;
  color: #b45309;
}

.closed {
  background: #fee2e2;
  color: #b91c1c;
}

.applicant-box {
  text-align: center;
  background: #eff6ff;
  border-radius: 18px;
  padding: 18px;
  min-width: 100px;
}

.applicant-box h5 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #2563eb;
}

.applicant-box span {
  color: #64748b;
  font-size: 0.9rem;
}

/* =========================
   BODY
========================= */

.description {
  color: #475569;
  line-height: 1.8;
  margin-bottom: 25px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 18px;
}

.detail-item {
  background: #f8fafc;
  border-radius: 14px;
  padding: 16px;
}

.label {
  display: block;
  font-size: 0.8rem;
  color: #64748b;
  margin-bottom: 8px;
}

.value {
  font-weight: 600;
  color: #0f172a;
}

/* =========================
   FOOTER
========================= */

.drive-footer {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 30px;
}

.drive-footer .btn {
  border-radius: 12px;
  padding: 11px 18px;
  font-weight: 600;
}

/* =========================
   LOADING
========================= */

.loading-section {
  text-align: center;
  padding: 80px 20px;
}

/* =========================
   EMPTY
========================= */

.empty-card {
  background: white;
  padding: 60px 30px;
  border-radius: 24px;
  text-align: center;
  box-shadow:
    0 8px 24px rgba(0,0,0,0.05);
}

.empty-card i {
  font-size: 4rem;
  color: #94a3b8;
}

.empty-card h4 {
  margin-top: 20px;
  font-weight: 700;
}

.empty-card p {
  margin-top: 10px;
  color: #64748b;
}

/* =========================
   MODAL
========================= */

.custom-modal {
  position: fixed;
  inset: 0;
  background: rgba(15,23,42,0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  z-index: 999;
}

.modal-card {
  width: 100%;
  max-width: 700px;
  background: white;
  border-radius: 24px;
  padding: 35px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.modal-header h4 {
  font-weight: 700;
}

.close-btn {
  border: none;
  background: none;
  font-size: 1.3rem;
  cursor: pointer;
}

.form-control {
  border-radius: 12px;
  padding: 13px 15px;
  min-height: 50px;
}

textarea.form-control {
  min-height: 140px;
  resize: none;
}

/* =========================
   ALERT
========================= */

.alert {
  border-radius: 14px;
  padding: 15px 18px;
}

/* =========================
   RESPONSIVE
========================= */

@media (max-width: 768px) {

  .detail-grid {
    grid-template-columns: 1fr;
  }

  .drive-top {
    flex-direction: column;
  }

  .drive-footer {
    flex-direction: column;
  }

  .drive-footer .btn {
    width: 100%;
  }

  .modal-card {
    padding: 25px;
  }

  .page-header h2 {
    font-size: 1.9rem;
  }

}

</style>