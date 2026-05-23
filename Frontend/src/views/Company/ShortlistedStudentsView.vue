<template>
  <div class="shortlisted-page">

    <div class="container py-5">

      <!-- PAGE HEADER -->

      <div class="page-header mb-4">

        <div>

          <h2>
            Shortlisted Students
          </h2>

          <p>
            View shortlisted and selected candidates for your placement drives.
          </p>

        </div>

        <router-link
          to="/company/dashboard"
          class="btn btn-outline-primary"
        >

          <i class="bi bi-arrow-left me-2"></i>

          Back Dashboard

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

      <!-- FILTER SECTION -->

      <div class="filter-card mb-4">

        <div class="row g-3 align-items-end">

          <!-- DRIVE -->

          <div class="col-lg-4">

            <label class="form-label">
              Placement Drive
            </label>

            <select
              class="form-select"
              v-model="selectedDrive"
              @change="fetchStudents"
            >

              <option value="">
                All Drives
              </option>

              <option
                v-for="drive in drives"
                :key="drive.id"
                :value="drive.id"
              >
                {{ drive.job_title }}
              </option>

            </select>

          </div>

          <!-- STATUS -->

          <div class="col-lg-4">

            <label class="form-label">
              Application Status
            </label>

            <select
              class="form-select"
              v-model="selectedStatus"
              @change="fetchStudents"
            >

              <option value="">
                All Status
              </option>

              <option value="Shortlisted">
                Shortlisted
              </option>

              <option value="Selected">
                Selected
              </option>

            </select>

          </div>

          <!-- SEARCH -->

          <div class="col-lg-4">

            <label class="form-label">
              Search Student
            </label>

            <input
              type="text"
              class="form-control"
              placeholder="Search by name or email"
              v-model="search"
            />

          </div>

        </div>

      </div>

      <!-- LOADING -->

      <div
        v-if="loading"
        class="loading-section"
      >

        <div class="spinner-border text-primary"></div>

        <p class="mt-3">
          Loading shortlisted students...
        </p>

      </div>

      <!-- EMPTY -->

      <div
        v-else-if="filteredStudents.length === 0"
        class="empty-card"
      >

        <i class="bi bi-people"></i>

        <h4>
          No Students Found
        </h4>

        <p>
          No shortlisted or selected students available.
        </p>

      </div>

      <!-- STUDENTS -->

      <div
        v-else
        class="row g-4"
      >

        <div
          class="col-lg-6"
          v-for="student in filteredStudents"
          :key="student.application_id"
        >

          <div class="student-card">

            <!-- TOP -->

            <div class="card-top">

              <div class="student-info">

                <div class="avatar">

                  {{ student.student_name.charAt(0) }}

                </div>

                <div>

                  <h4>
                    {{ student.student_name }}
                  </h4>

                  <p>
                    {{ student.student_email }}
                  </p>

                </div>

              </div>

              <span
                class="status-badge"
                :class="student.status === 'Selected'
                  ? 'selected'
                  : 'shortlisted'
                "
              >

                {{ student.status }}

              </span>

            </div>

            <!-- DRIVE -->

            <div class="drive-box">

              <i class="bi bi-briefcase-fill me-2"></i>

              {{ student.job_title }}

            </div>

            <!-- DETAILS -->

            <div class="details-grid">

              <div class="detail-item">

                <span class="label">
                  Branch
                </span>

                <span class="value">
                  {{ student.branch }}
                </span>

              </div>

              <div class="detail-item">

                <span class="label">
                  CGPA
                </span>

                <span class="value">
                  {{ student.cgpa }}
                </span>

              </div>

              <div class="detail-item">

                <span class="label">
                  Passing Year
                </span>

                <span class="value">
                  {{ student.year }}
                </span>

              </div>

              <div class="detail-item">

                <span class="label">
                  Applied On
                </span>

                <span class="value">
                  {{ formatDate(student.application_date) }}
                </span>

              </div>

            </div>

            <!-- INTERVIEW -->

            <div
              v-if="student.interview_date"
              class="interview-box"
            >

              <i class="bi bi-calendar-event me-2"></i>

              Interview :
              {{ formatDateTime(student.interview_date) }}

            </div>

            <!-- ACTIONS -->

            <div class="action-section">

              <button
                class="btn btn-outline-success"
                @click="markSelected(student)"
                v-if="student.status !== 'Selected'"
              >

                <i class="bi bi-check-circle me-2"></i>

                Mark Selected

              </button>

              <button
                class="btn btn-outline-danger"
                @click="markRejected(student)"
              >

                <i class="bi bi-x-circle me-2"></i>

                Reject

              </button>

              <a
                v-if="student.resume"
                :href="student.resume"
                target="_blank"
                class="btn btn-outline-primary"
              >

                <i class="bi bi-file-earmark-arrow-down me-2"></i>

                Resume

              </a>

            </div>

          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<script>
import axios from "axios"

export default {

  name: "ShortlistedStudentsView",

  data() {

    return {

      loading: false,

      success: false,

      message: "",

      students: [],

      drives: [],

      selectedDrive: "",

      selectedStatus: "",

      search: ""

    }

  },

  computed: {

    filteredStudents() {

      return this.students.filter(student => {

        const matchesSearch =

          student.student_name
            .toLowerCase()
            .includes(this.search.toLowerCase())

          ||

          student.student_email
            .toLowerCase()
            .includes(this.search.toLowerCase())

        return matchesSearch

      })

    }

  },

  mounted() {

    this.fetchDrives()

    this.fetchStudents()

  },

  methods: {

    async fetchDrives() {

      try {

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

        console.log(error)

      }

    },

    async fetchStudents() {

      try {

        this.loading = true

        const token = localStorage.getItem("token")

        let url =
          "http://127.0.0.1:5000/api/company/shortlisted-students"

        const params = {}

        if (this.selectedDrive) {

          params.drive_id = this.selectedDrive

        }

        if (this.selectedStatus) {

          params.status = this.selectedStatus

        }

        const response = await axios.get(

          url,

          {

            params,

            headers: {

              Authorization: `Bearer ${token}`

            }

          }

        )

        this.students = response.data

      }

      catch (error) {

        this.message =
          error.response?.data?.message ||
          "Failed to load students."

      }

      finally {

        this.loading = false

      }

    },

    async markSelected(student) {

      try {

        const token = localStorage.getItem("token")

        const response = await axios.put(

          `http://127.0.0.1:5000/api/company/application/update-status/${student.application_id}`,

          {

            status: "Selected"

          },

          {

            headers: {

              Authorization: `Bearer ${token}`

            }

          }

        )

        student.status = "Selected"

        this.success = true

        this.message = response.data.message

      }

      catch (error) {

        this.success = false

        this.message =
          error.response?.data?.message ||
          "Failed to update status."

      }

    },

    async markRejected(student) {

      try {

        const token = localStorage.getItem("token")

        const response = await axios.put(

          `http://127.0.0.1:5000/api/company/application/update-status/${student.application_id}`,

          {

            status: "Rejected"

          },

          {

            headers: {

              Authorization: `Bearer ${token}`

            }

          }

        )

        this.students =
          this.students.filter(

            item =>
              item.application_id !==
              student.application_id

          )

        this.success = true

        this.message = response.data.message

      }

      catch (error) {

        this.success = false

        this.message =
          error.response?.data?.message ||
          "Failed to reject student."

      }

    },

    formatDate(date) {

      return new Date(date).toLocaleDateString()

    },

    formatDateTime(date) {

      return new Date(date).toLocaleString()

    }

  }

}
</script>

<style scoped>

/* =========================
   PAGE
========================= */

.shortlisted-page {
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
   FILTER
========================= */

.filter-card {
  background: white;
  border-radius: 22px;
  padding: 25px;
  box-shadow:
    0 8px 24px rgba(0,0,0,0.05);
}

.form-label {
  font-weight: 600;
  margin-bottom: 10px;
}

.form-select,
.form-control {
  min-height: 50px;
  border-radius: 12px;
}

/* =========================
   STUDENT CARD
========================= */

.student-card {
  background: white;
  border-radius: 24px;
  padding: 28px;
  box-shadow:
    0 8px 24px rgba(0,0,0,0.05);
  height: 100%;
}

/* =========================
   TOP
========================= */

.card-top {
  display: flex;
  justify-content: space-between;
  gap: 15px;
  margin-bottom: 22px;
}

.student-info {
  display: flex;
  gap: 15px;
}

.avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #2563eb;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.4rem;
}

.student-info h4 {
  font-weight: 700;
  margin-bottom: 5px;
}

.student-info p {
  color: #64748b;
  margin: 0;
  word-break: break-word;
}

/* =========================
   STATUS
========================= */

.status-badge {
  padding: 8px 14px;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 600;
  height: fit-content;
}

.shortlisted {
  background: #fef3c7;
  color: #b45309;
}

.selected {
  background: #dcfce7;
  color: #15803d;
}

/* =========================
   DRIVE
========================= */

.drive-box {
  background: #eff6ff;
  color: #1d4ed8;
  padding: 14px 16px;
  border-radius: 14px;
  font-weight: 600;
  margin-bottom: 22px;
}

/* =========================
   DETAILS
========================= */

.details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.detail-item {
  background: #f8fafc;
  border-radius: 14px;
  padding: 16px;
}

.label {
  display: block;
  color: #64748b;
  font-size: 0.8rem;
  margin-bottom: 8px;
}

.value {
  font-weight: 600;
  color: #0f172a;
}

/* =========================
   INTERVIEW
========================= */

.interview-box {
  margin-top: 22px;
  background: #f8fafc;
  border-radius: 14px;
  padding: 15px 16px;
  color: #1e293b;
  font-weight: 500;
}

/* =========================
   ACTIONS
========================= */

.action-section {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 24px;
}

.btn {
  border-radius: 12px;
  font-weight: 600;
}

/* =========================
   EMPTY
========================= */

.empty-card {
  background: white;
  border-radius: 24px;
  padding: 70px 30px;
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
  color: #64748b;
  margin-top: 10px;
}

/* =========================
   LOADING
========================= */

.loading-section {
  text-align: center;
  padding: 80px 20px;
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

  .details-grid {
    grid-template-columns: 1fr;
  }

  .card-top {
    flex-direction: column;
  }

  .action-section {
    flex-direction: column;
  }

  .action-section .btn {
    width: 100%;
  }

  .page-header h2 {
    font-size: 1.9rem;
  }

}

</style>