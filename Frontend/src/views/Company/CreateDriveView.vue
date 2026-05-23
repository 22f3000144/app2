<template>
  <div class="create-drive-page">

    <div class="container py-5">

      <!-- PAGE HEADER -->

      <div class="page-header mb-5">

        <div>
          <h2>Create Placement Drive</h2>

          <p>
            Create and publish new placement opportunities
            for eligible students.
          </p>
        </div>

        <router-link
          to="/company/dashboard"
          class="btn btn-outline-primary"
        >
          <i class="bi bi-arrow-left"></i>
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

      <!-- FORM CARD -->

      <div class="form-card">

        <form @submit.prevent="createDrive">

          <div class="row">

            <!-- JOB TITLE -->

            <div class="col-md-6 mb-4">

              <label class="form-label">
                Job Title
              </label>

              <input
                type="text"
                class="form-control"
                placeholder="Frontend Developer"
                v-model="form.job_title"
              />

            </div>

            <!-- REQUIRED BRANCH -->

            <div class="col-md-6 mb-4">

              <label class="form-label">
                Required Branch
              </label>

              <select
                class="form-select"
                v-model="form.required_branch"
              >

                <option value="">
                  Select Branch
                </option>

                <option
                  v-for="branch in branches"
                  :key="branch"
                  :value="branch"
                >
                  {{ branch }}
                </option>

              </select>

            </div>

            <!-- MIN CGPA -->

            <div class="col-md-6 mb-4">

              <label class="form-label">
                Minimum CGPA
              </label>

              <input
                type="number"
                step="0.1"
                min="0"
                max="10"
                class="form-control"
                placeholder="7.0"
                v-model="form.min_cgpa"
              />

            </div>

            <!-- PASSING YEAR -->

            <div class="col-md-6 mb-4">

              <label class="form-label">
                Passing Year
              </label>

              <select
                class="form-select"
                v-model="form.passing_year"
              >

                <option value="">
                  Select Year
                </option>

                <option
                  v-for="year in years"
                  :key="year"
                  :value="year"
                >
                  {{ year }}
                </option>

              </select>

            </div>

            <!-- DEADLINE -->

            <div class="col-md-6 mb-4">

              <label class="form-label">
                Application Deadline
              </label>

              <input
                type="date"
                class="form-control"
                v-model="form.application_deadline"
              />

            </div>

            <!-- STATUS -->

            <div class="col-md-6 mb-4">

              <label class="form-label">
                Drive Status
              </label>

              <input
                type="text"
                class="form-control bg-light"
                value="Pending Admin Approval"
                disabled
              />

            </div>

            <!-- JOB DESCRIPTION -->

            <div class="col-12 mb-4">

              <label class="form-label">
                Job Description
              </label>

              <textarea
                rows="7"
                class="form-control"
                placeholder="Describe job role, skills, salary package, interview rounds etc."
                v-model="form.job_description"
              ></textarea>

            </div>

          </div>

          <!-- SUBMIT BUTTON -->

          <div class="submit-area">

            <button
              type="submit"
              class="btn btn-primary submit-btn"
              :disabled="loading"
            >

              <span
                v-if="loading"
                class="spinner-border spinner-border-sm me-2"
              ></span>

              {{ loading ? "Creating Drive..." : "Create Placement Drive" }}

            </button>

          </div>

        </form>

      </div>

      <!-- INFO SECTION -->

      <div class="info-section mt-5">

        <div class="row g-4">

          <div class="col-md-4">

            <div class="info-card">

              <div class="icon-box blue">
                <i class="bi bi-shield-check"></i>
              </div>

              <h5>Admin Approval</h5>

              <p>
                Every placement drive requires admin approval
                before students can apply.
              </p>

            </div>

          </div>

          <div class="col-md-4">

            <div class="info-card">

              <div class="icon-box green">
                <i class="bi bi-people-fill"></i>
              </div>

              <h5>Eligibility Filter</h5>

              <p>
                Students will only see drives matching
                branch, CGPA, and passing year criteria.
              </p>

            </div>

          </div>

          <div class="col-md-4">

            <div class="info-card">

              <div class="icon-box orange">
                <i class="bi bi-clock-history"></i>
              </div>

              <h5>Track Applications</h5>

              <p>
                View applicants, shortlist candidates,
                and manage recruitment workflow easily.
              </p>

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

  name: "CreateDriveView",

  data() {

    return {

      loading: false,

      success: false,

      message: "",

      form: {

        job_title: "",

        job_description: "",

        required_branch: "",

        min_cgpa: "",

        passing_year: "",

        application_deadline: ""

      },

      branches: [

        "Computer Science",
        "Information Technology",
        "Electronics",
        "Electrical",
        "Mechanical",
        "Civil",
        "Data Science",
        "Mathematics",
        "MBA",
        "All Branches"

      ],

      years: [

        2024,
        2025,
        2026,
        2027,
        2028

      ]

    }

  },

  methods: {

    async createDrive() {

      this.message = ""

      this.success = false

      if (

        !this.form.job_title ||
        !this.form.job_description ||
        !this.form.required_branch ||
        !this.form.min_cgpa ||
        !this.form.passing_year ||
        !this.form.application_deadline

      ) {

        this.message = "Please fill all required fields."
        return

      }

      try {

        this.loading = true

        const token = localStorage.getItem("token")

        const response = await axios.post(

          "http://127.0.0.1:5000/api/company/drive/create",

          this.form,

          {

            headers: {

              Authorization: `Bearer ${token}`

            }

          }

        )

        this.success = true

        this.message = response.data.message

        // RESET FORM

        this.form = {

          job_title: "",

          job_description: "",

          required_branch: "",

          min_cgpa: "",

          passing_year: "",

          application_deadline: ""

        }

      }

      catch (error) {

        this.success = false

        if (error.response) {

          this.message =
            error.response.data.message ||
            "Failed to create drive."

        }

        else {

          this.message =
            "Server connection failed."

        }

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

.create-drive-page {
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
  font-size: 2.2rem;
  font-weight: 700;
  color: #0f172a;
}

.page-header p {
  margin-top: 10px;
  color: #64748b;
}

/* =========================
   FORM CARD
========================= */

.form-card {
  background: white;
  border-radius: 24px;
  padding: 40px;
  box-shadow:
    0 10px 30px rgba(0,0,0,0.06);
}

/* =========================
   FORM
========================= */

.form-label {
  font-weight: 600;
  margin-bottom: 10px;
  color: #1e293b;
}

.form-control,
.form-select {
  border-radius: 14px;
  padding: 14px 16px;
  border: 1px solid #dbe3ef;
  min-height: 52px;
  box-shadow: none;
}

.form-control:focus,
.form-select:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 0.15rem rgba(37,99,235,0.15);
}

textarea.form-control {
  min-height: 180px;
  resize: none;
}

.submit-area {
  margin-top: 15px;
}

.submit-btn {
  padding: 14px 28px;
  border-radius: 14px;
  font-weight: 600;
  min-width: 240px;
}

/* =========================
   INFO SECTION
========================= */

.info-card {
  background: white;
  border-radius: 22px;
  padding: 30px;
  height: 100%;
  box-shadow:
    0 8px 24px rgba(0,0,0,0.05);
  transition: 0.3s ease;
}

.info-card:hover {
  transform: translateY(-6px);
}

.icon-box {
  width: 65px;
  height: 65px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.icon-box i {
  font-size: 1.7rem;
  color: white;
}

.blue {
  background: #2563eb;
}

.green {
  background: #10b981;
}

.orange {
  background: #f59e0b;
}

.info-card h5 {
  font-weight: 700;
  margin-bottom: 14px;
  color: #0f172a;
}

.info-card p {
  color: #64748b;
  line-height: 1.7;
}

/* =========================
   ALERT
========================= */

.alert {
  border-radius: 14px;
  padding: 16px 18px;
  margin-bottom: 25px;
}

/* =========================
   RESPONSIVE
========================= */

@media (max-width: 768px) {

  .form-card {
    padding: 25px;
  }

  .page-header h2 {
    font-size: 1.8rem;
  }

  .submit-btn {
    width: 100%;
  }

}

</style>