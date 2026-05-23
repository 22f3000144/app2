<template>
  <div class="applicants-page">

    <div class="container py-5">

      <!-- PAGE HEADER -->

      <div class="page-header mb-4">

        <div>

          <h2>
            Drive Applicants
          </h2>

          <p>
            View and manage student applications for this placement drive.
          </p>

        </div>

        <router-link
          to="/company/drives"
          class="btn btn-outline-primary"
        >

          <i class="bi bi-arrow-left me-2"></i>

          Back To Drives

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
          Loading applicants...
        </p>

      </div>

      <!-- EMPTY -->

      <div
        v-else-if="applicants.length === 0"
        class="empty-card"
      >

        <i class="bi bi-people"></i>

        <h4>
          No Applications Found
        </h4>

        <p>
          Students have not applied for this placement drive yet.
        </p>

      </div>

      <!-- APPLICANTS -->

      <div
        v-else
        class="row g-4"
      >

        <div
          class="col-lg-6"
          v-for="applicant in applicants"
          :key="applicant.application_id"
        >

          <div class="applicant-card">

            <!-- TOP -->

            <div class="card-top">

              <div class="student-info">

                <div class="avatar">

                  {{ applicant.student_name.charAt(0) }}

                </div>

                <div>

                  <h4>
                    {{ applicant.student_name }}
                  </h4>

                  <p>
                    {{ applicant.student_email }}
                  </p>

                </div>

              </div>

              <span
                class="status-badge"
                :class="getStatusClass(applicant.status)"
              >

                {{ applicant.status }}

              </span>

            </div>

            <!-- DETAILS -->

            <div class="details-grid">

              <div class="detail-box">

                <span class="label">
                  Branch
                </span>

                <span class="value">
                  {{ applicant.branch }}
                </span>

              </div>

              <div class="detail-box">

                <span class="label">
                  CGPA
                </span>

                <span class="value">
                  {{ applicant.cgpa }}
                </span>

              </div>

              <div class="detail-box">

                <span class="label">
                  Passing Year
                </span>

                <span class="value">
                  {{ applicant.year }}
                </span>

              </div>

              <div class="detail-box">

                <span class="label">
                  Applied On
                </span>

                <span class="value">
                  {{ formatDate(applicant.application_date) }}
                </span>

              </div>

            </div>

            <!-- INTERVIEW -->

            <div
              v-if="applicant.interview_date"
              class="interview-box"
            >

              <i class="bi bi-calendar-event me-2"></i>

              Interview Scheduled :
              {{ formatDateTime(applicant.interview_date) }}

            </div>

            <!-- ACTIONS -->

            <div class="action-section">

              <select
                class="form-select"
                v-model="applicant.status"
              >

                <option value="Applied">
                  Applied
                </option>

                <option value="Shortlisted">
                  Shortlisted
                </option>

                <option value="Selected">
                  Selected
                </option>

                <option value="Rejected">
                  Rejected
                </option>

              </select>

              <button
                class="btn btn-primary"
                @click="updateStatus(applicant)"
              >

                Update Status

              </button>

            </div>

            <!-- INTERVIEW -->

            <div class="schedule-section">

              <input
                type="datetime-local"
                class="form-control"
                v-model="applicant.interview_input"
              />

              <button
                class="btn btn-outline-dark"
                @click="scheduleInterview(applicant)"
              >

                Schedule Interview

              </button>

            </div>

            <!-- RESUME -->

            <div class="resume-section">

              <a
                v-if="applicant.resume"
                :href="applicant.resume"
                target="_blank"
                class="btn btn-outline-success"
              >

                <i class="bi bi-file-earmark-arrow-down me-2"></i>

                View Resume

              </a>

              <span
                v-else
                class="text-muted"
              >
                Resume Not Uploaded
              </span>

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

  name: "ApplicantsView",

  data() {

    return {

      loading: false,

      success: false,

      message: "",

      applicants: []

    }

  },

  mounted() {

    this.fetchApplicants()

  },

  methods: {

    async fetchApplicants() {

      try {

        this.loading = true

        const token = localStorage.getItem("token")

        const driveId = this.$route.params.id

        const response = await axios.get(

          `http://127.0.0.1:5000/api/company/applicants/${driveId}`,

          {

            headers: {

              Authorization: `Bearer ${token}`

            }

          }

        )

        this.applicants = response.data.map(

          applicant => ({

            ...applicant,

            interview_input: ""

          })

        )

      }

      catch (error) {

        this.success = false

        this.message =
          error.response?.data?.message ||
          "Failed to load applicants."

      }

      finally {

        this.loading = false

      }

    },

    async updateStatus(applicant) {

      try {

        const token = localStorage.getItem("token")

        const response = await axios.put(

          `http://127.0.0.1:5000/api/company/application/status/${applicant.application_id}`,

          {

            status: applicant.status

          },

          {

            headers: {

              Authorization: `Bearer ${token}`

            }

          }

        )

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

    async scheduleInterview(applicant) {

      if (!applicant.interview_input) {

        this.success = false

        this.message =
          "Please select interview date and time."

        return

      }

      try {

        const token = localStorage.getItem("token")

        const formattedDate =
          applicant.interview_input.replace("T", " ") + ":00"

        const response = await axios.put(

          `http://127.0.0.1:5000/api/company/interview/schedule/${applicant.application_id}`,

          {

            interview_date: formattedDate

          },

          {

            headers: {

              Authorization: `Bearer ${token}`

            }

          }

        )

        this.success = true

        this.message = response.data.message

        applicant.interview_date = formattedDate

        applicant.interview_input = ""

      }

      catch (error) {

        this.success = false

        this.message =
          error.response?.data?.message ||
          "Failed to schedule interview."

      }

    },

    formatDate(date) {

      return new Date(date).toLocaleDateString()

    },

    formatDateTime(date) {

      return new Date(date).toLocaleString()

    },

    getStatusClass(status) {

      if (status === "Selected") {

        return "selected"

      }

      else if (status === "Shortlisted") {

        return "shortlisted"

      }

      else if (status === "Rejected") {

        return "rejected"

      }

      else {

        return "applied"

      }

    }

  }

}
</script>

<style scoped>

.applicants-page {
  min-height: 100vh;
  background: #f5f7fb;
}

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

.applicant-card {
  background: white;
  border-radius: 24px;
  padding: 28px;
  box-shadow:
    0 8px 24px rgba(0,0,0,0.05);
  height: 100%;
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 15px;
  margin-bottom: 25px;
}

.student-info {
  display: flex;
  gap: 16px;
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
  font-size: 1.5rem;
  font-weight: 700;
}

.student-info h4 {
  font-weight: 700;
  margin-bottom: 5px;
  color: #0f172a;
}

.student-info p {
  color: #64748b;
  margin: 0;
  word-break: break-word;
}

.status-badge {
  padding: 8px 14px;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 600;
}

.applied {
  background: #dbeafe;
  color: #1d4ed8;
}

.shortlisted {
  background: #fef3c7;
  color: #b45309;
}

.selected {
  background: #dcfce7;
  color: #15803d;
}

.rejected {
  background: #fee2e2;
  color: #b91c1c;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 25px;
}

.detail-box {
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

.interview-box {
  background: #eff6ff;
  padding: 15px 18px;
  border-radius: 14px;
  margin-bottom: 22px;
  color: #1e3a8a;
  font-weight: 500;
}

.action-section,
.schedule-section {
  display: flex;
  gap: 12px;
  margin-bottom: 18px;
}

.form-select,
.form-control {
  border-radius: 12px;
  min-height: 48px;
}

.btn {
  border-radius: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.resume-section {
  margin-top: 10px;
}

.loading-section {
  text-align: center;
  padding: 80px 20px;
}

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

.alert {
  border-radius: 14px;
  padding: 15px 18px;
}

@media (max-width: 768px) {

  .details-grid {
    grid-template-columns: 1fr;
  }

  .card-top {
    flex-direction: column;
  }

  .action-section,
  .schedule-section {
    flex-direction: column;
  }

  .action-section .btn,
  .schedule-section .btn {
    width: 100%;
  }

  .page-header h2 {
    font-size: 1.9rem;
  }

}

</style>