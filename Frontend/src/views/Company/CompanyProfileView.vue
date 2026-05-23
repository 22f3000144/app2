<template>
  <div class="company-profile-page">

    <div class="container py-5">

      <!-- PAGE HEADER -->

      <div class="page-header mb-4">

        <div>

          <h2>
            Company Profile
          </h2>

          <p>
            View your company information and approval status.
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

      <!-- LOADING -->

      <div
        v-if="loading"
        class="loading-section"
      >

        <div class="spinner-border text-primary"></div>

        <p class="mt-3">
          Loading company profile...
        </p>

      </div>

      <!-- PROFILE -->

      <div
        v-else
        class="row g-4"
      >

        <!-- LEFT -->

        <div class="col-lg-4">

          <div class="profile-card">

            <div class="company-avatar">

              {{ company.name?.charAt(0) }}

            </div>

            <h3>
              {{ company.name }}
            </h3>

            <p>
              {{ company.email }}
            </p>

            <span
              class="status-badge"
              :class="company.approved ? 'approved' : 'pending'"
            >

              {{ company.approved
                ? "Approved Company"
                : "Pending Approval"
              }}

            </span>

            <div
              class="active-status"
              :class="company.active ? 'active' : 'inactive'"
            >

              <i
                class="bi"
                :class="company.active
                  ? 'bi-check-circle-fill'
                  : 'bi-x-circle-fill'
                "
              ></i>

              {{ company.active
                ? "Account Active"
                : "Account Deactivated"
              }}

            </div>

          </div>

        </div>

        <!-- RIGHT -->

        <div class="col-lg-8">

          <div class="details-card">

            <div class="card-header-custom">

              <h4>
                Company Information
              </h4>

            </div>

            <div class="details-grid">

              <!-- COMPANY NAME -->

              <div class="detail-item">

                <span class="label">
                  Company Name
                </span>

                <span class="value">
                  {{ company.name }}
                </span>

              </div>

              <!-- EMAIL -->

              <div class="detail-item">

                <span class="label">
                  Official Email
                </span>

                <span class="value">
                  {{ company.email }}
                </span>

              </div>

              <!-- HR CONTACT -->

              <div class="detail-item">

                <span class="label">
                  HR Contact
                </span>

                <span class="value">
                  {{ company.hr_contact || "Not Available" }}
                </span>

              </div>

              <!-- WEBSITE -->

              <div class="detail-item">

                <span class="label">
                  Company Website
                </span>

                <a
                  v-if="company.website"
                  :href="company.website"
                  target="_blank"
                  class="website-link"
                >
                  {{ company.website }}
                </a>

                <span
                  v-else
                  class="value"
                >
                  Not Available
                </span>

              </div>

              <!-- TOTAL DRIVES -->

              <div class="detail-item">

                <span class="label">
                  Total Drives
                </span>

                <span class="value">
                  {{ stats.total_drives }}
                </span>

              </div>

              <!-- APPROVED DRIVES -->

              <div class="detail-item">

                <span class="label">
                  Approved Drives
                </span>

                <span class="value">
                  {{ stats.approved_drives }}
                </span>

              </div>

              <!-- PENDING DRIVES -->

              <div class="detail-item">

                <span class="label">
                  Pending Drives
                </span>

                <span class="value">
                  {{ stats.pending_drives }}
                </span>

              </div>

              <!-- TOTAL APPLICATIONS -->

              <div class="detail-item">

                <span class="label">
                  Total Applications
                </span>

                <span class="value">
                  {{ stats.total_applications }}
                </span>

              </div>

            </div>

          </div>

          <!-- INFO SECTION -->

          <div class="info-card mt-4">

            <h5>
              Placement Guidelines
            </h5>

            <div class="guideline-list">

              <div class="guideline-item">

                <i class="bi bi-check-circle-fill"></i>

                <span>
                  Placement drives require admin approval before publishing.
                </span>

              </div>

              <div class="guideline-item">

                <i class="bi bi-check-circle-fill"></i>

                <span>
                  Keep job descriptions and eligibility criteria accurate.
                </span>

              </div>

              <div class="guideline-item">

                <i class="bi bi-check-circle-fill"></i>

                <span>
                  Update student application status regularly.
                </span>

              </div>

              <div class="guideline-item">

                <i class="bi bi-check-circle-fill"></i>

                <span>
                  Schedule interviews only after shortlisting candidates.
                </span>

              </div>

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

  name: "CompanyProfileView",

  data() {

    return {

      loading: false,

      success: false,

      message: "",

      company: {},

      stats: {}

    }

  },

  mounted() {

    this.fetchProfile()

  },

  methods: {

    async fetchProfile() {

      try {

        this.loading = true

        const token = localStorage.getItem("token")

        const response = await axios.get(

          "http://127.0.0.1:5000/api/company/dashboard",

          {

            headers: {

              Authorization: `Bearer ${token}`

            }

          }

        )

        this.company = response.data.company

        this.stats = response.data.stats

      }

      catch (error) {

        this.success = false

        this.message =
          error.response?.data?.message ||
          "Failed to load company profile."

      }

      finally {

        this.loading = false

      }

    }

  }

}
</script>

<style scoped>

/* =========================
   PAGE
========================= */

.company-profile-page {
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
   PROFILE CARD
========================= */

.profile-card {
  background: white;
  border-radius: 24px;
  padding: 35px 25px;
  text-align: center;
  box-shadow:
    0 8px 24px rgba(0,0,0,0.05);
  height: 100%;
}

.company-avatar {
  width: 110px;
  height: 110px;
  border-radius: 50%;
  background: linear-gradient(
    135deg,
    #2563eb,
    #1d4ed8
  );
  color: white;
  font-size: 2.8rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: auto;
  margin-bottom: 25px;
}

.profile-card h3 {
  font-weight: 700;
  color: #0f172a;
}

.profile-card p {
  color: #64748b;
  margin-top: 8px;
  word-break: break-word;
}

/* =========================
   STATUS
========================= */

.status-badge {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 18px;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 600;
}

.approved {
  background: #dcfce7;
  color: #15803d;
}

.pending {
  background: #fef3c7;
  color: #b45309;
}

.active-status {
  margin-top: 18px;
  font-weight: 600;
}

.active {
  color: #15803d;
}

.inactive {
  color: #b91c1c;
}

/* =========================
   DETAILS CARD
========================= */

.details-card,
.info-card {
  background: white;
  border-radius: 24px;
  padding: 35px;
  box-shadow:
    0 8px 24px rgba(0,0,0,0.05);
}

.card-header-custom {
  margin-bottom: 30px;
}

.card-header-custom h4 {
  font-weight: 700;
  color: #0f172a;
}

/* =========================
   GRID
========================= */

.details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.detail-item {
  background: #f8fafc;
  border-radius: 16px;
  padding: 18px;
}

.label {
  display: block;
  color: #64748b;
  font-size: 0.82rem;
  margin-bottom: 10px;
}

.value {
  font-weight: 600;
  color: #0f172a;
  word-break: break-word;
}

.website-link {
  color: #2563eb;
  font-weight: 600;
  text-decoration: none;
  word-break: break-word;
}

.website-link:hover {
  text-decoration: underline;
}

/* =========================
   GUIDELINES
========================= */

.info-card h5 {
  font-weight: 700;
  margin-bottom: 25px;
  color: #0f172a;
}

.guideline-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.guideline-item {
  display: flex;
  gap: 14px;
  align-items: flex-start;
}

.guideline-item i {
  color: #10b981;
  margin-top: 2px;
}

.guideline-item span {
  color: #475569;
  line-height: 1.7;
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

@media (max-width: 991px) {

  .details-grid {
    grid-template-columns: 1fr;
  }

}

@media (max-width: 768px) {

  .page-header h2 {
    font-size: 1.9rem;
  }

  .details-card,
  .info-card {
    padding: 25px;
  }

}

</style>