<template>
  <div class="create-drive-page">

    <!-- Header -->
    <div class="page-header">

      <div>
        <h2>Create Placement Drive</h2>

        <p>
          Publish new campus recruitment opportunities
        </p>
      </div>

      <router-link
        to="/company/dashboard"
        class="back-btn"
      >
        ← Back
      </router-link>

    </div>

    <!-- Form Card -->
    <div class="form-card">

      <form @submit.prevent="createDrive">

        <!-- Job Title -->
        <div class="form-group">

          <label>Job Title</label>

          <input
            type="text"
            v-model="form.job_title"
            placeholder="Enter job title"
            required
          />

        </div>

        <!-- Job Description -->
        <div class="form-group">

          <label>Job Description</label>

          <textarea
            rows="6"
            v-model="form.job_description"
            placeholder="Describe job role, responsibilities, package, etc."
            required
          ></textarea>

        </div>

        <!-- Grid -->
        <div class="form-grid">

          <!-- Branch -->
          <div class="form-group">

            <label>Required Branch</label>

            <select
              v-model="form.required_branch"
              required
            >
              <option value="">
                Select Branch
              </option>

              <option value="CSE">
                CSE
              </option>

              <option value="IT">
                IT
              </option>

              <option value="ECE">
                ECE
              </option>

              <option value="EEE">
                EEE
              </option>

              <option value="ME">
                Mechanical
              </option>

              <option value="CE">
                Civil
              </option>

              <option value="ALL">
                All Branches
              </option>

            </select>

          </div>

          <!-- CGPA -->
          <div class="form-group">

            <label>Minimum CGPA</label>

            <input
              type="number"
              step="0.1"
              min="0"
              max="10"
              v-model="form.min_cgpa"
              placeholder="e.g. 7.5"
              required
            />

          </div>

          <!-- Passing Year -->
          <div class="form-group">

            <label>Passing Year</label>

            <input
              type="number"
              v-model="form.passing_year"
              placeholder="e.g. 2027"
              required
            />

          </div>

          <!-- Deadline -->
          <div class="form-group">

            <label>Application Deadline</label>

            <input
              type="date"
              v-model="form.application_deadline"
              required
            />

          </div>

        </div>

        <!-- Buttons -->
        <div class="button-group">

          <button
            type="submit"
            class="submit-btn"
            :disabled="loading"
          >

            <span v-if="loading">
              Creating...
            </span>

            <span v-else>
              Create Placement Drive
            </span>

          </button>

          <button
            type="button"
            class="cancel-btn"
            @click="$router.push('/company/dashboard')"
          >
            Cancel
          </button>

        </div>

      </form>

    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {

  name: "CreateDriveView",

  data() {

    return {

      loading: false,

      form: {

        job_title: "",
        job_description: "",
        required_branch: "",
        min_cgpa: "",
        passing_year: "",
        application_deadline: ""

      }

    };

  },

  methods: {

    async createDrive() {

      try {

        this.loading = true;

        const token = localStorage.getItem(
          "token"
        );

        const response = await axios.post(

          "http://127.0.0.1:5000/api/company/drives",

          this.form,

          {

            headers: {

              Authorization:
                `Bearer ${token}`

            }

          }

        );

        alert(
          response.data.message ||
          "Drive created successfully."
        );

        this.$router.push(
          "/company/dashboard"
        );

      }

      catch (error) {

        console.error(error);

        alert(

          error.response?.data?.message ||

          "Failed to create drive."

        );

      }

      finally {

        this.loading = false;

      }

    }

  }

};
</script>

<style scoped>

.create-drive-page {

  min-height: 100vh;
  padding: 30px;
  background:
    linear-gradient(
      135deg,
      #fff5f8,
      #f5f3ff
    );

}

/* =========================
   HEADER
========================= */

.page-header {

  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  gap: 20px;
  flex-wrap: wrap;

}

.page-header h2 {

  margin: 0;
  font-size: 34px;
  color: #312e81;

}

.page-header p {

  margin-top: 8px;
  color: #64748b;

}

.back-btn {

  text-decoration: none;

  background: white;
  color: #7c3aed;

  border: 2px solid #7c3aed;

  padding: 12px 18px;
  border-radius: 12px;

  font-weight: 600;
  transition: 0.3s;

}

.back-btn:hover {

  background: #7c3aed;
  color: white;

}

/* =========================
   FORM CARD
========================= */

.form-card {

  max-width: 1000px;
  margin: auto;

  background: white;
  padding: 35px;

  border-radius: 28px;

  box-shadow:
    0 20px 50px rgba(124, 58, 237, 0.08);

}

/* =========================
   FORM
========================= */

.form-group {

  margin-bottom: 24px;

}

.form-group label {

  display: block;
  margin-bottom: 10px;

  font-weight: 700;
  color: #334155;

}

.form-group input,
.form-group textarea,
.form-group select {

  width: 100%;

  padding: 14px 16px;

  border: 1px solid #dbeafe;

  border-radius: 14px;

  font-size: 15px;
  outline: none;

  transition: 0.3s;
  background: #fafafa;

}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {

  border-color: #7c3aed;

  box-shadow:
    0 0 0 4px rgba(124, 58, 237, 0.08);

  background: white;

}

.form-grid {

  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(220px, 1fr));

  gap: 20px;

}

/* =========================
   BUTTONS
========================= */

.button-group {

  display: flex;
  gap: 16px;
  margin-top: 10px;
  flex-wrap: wrap;

}

.submit-btn,
.cancel-btn {

  border: none;
  padding: 14px 24px;
  border-radius: 14px;

  font-size: 15px;
  font-weight: 700;

  cursor: pointer;
  transition: 0.3s;

}

.submit-btn {

  background:
    linear-gradient(
      135deg,
      #7c3aed,
      #dc2626
    );

  color: white;

  box-shadow:
    0 12px 25px rgba(124, 58, 237, 0.2);

}

.submit-btn:hover {

  transform: translateY(-2px);

}

.submit-btn:disabled {

  opacity: 0.7;
  cursor: not-allowed;

}

.cancel-btn {

  background: #f1f5f9;
  color: #334155;

}

.cancel-btn:hover {

  background: #e2e8f0;

}

/* =========================
   RESPONSIVE
========================= */

@media (max-width: 768px) {

  .create-drive-page {

    padding: 18px;

  }

  .page-header {

    flex-direction: column;
    align-items: flex-start;

  }

  .page-header h2 {

    font-size: 28px;

  }

  .form-card {

    padding: 24px;

  }

  .button-group {

    flex-direction: column;

  }

  .submit-btn,
  .cancel-btn {

    width: 100%;

  }

}

</style>