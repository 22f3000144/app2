<template>
  <div class="applicants-page">

    <!-- Header -->
    <div class="page-header">

      <div>

        <h2>Drive Applicants</h2>

        <p>
          View and manage student applications
        </p>

      </div>

      <router-link
        to="/company/drives"
        class="back-btn"
      >
        ← Back
      </router-link>

    </div>

    <!-- Filters -->
    <div class="filter-section">

      <input
        type="text"
        v-model="search"
        placeholder="Search by student name, branch, skills..."
      />

      <select v-model="statusFilter">

        <option value="">
          All Status
        </option>

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

    </div>

    <!-- Loading -->
    <div
      v-if="loading"
      class="loading-box"
    >
      Loading applicants...
    </div>

    <!-- Empty -->
    <div
      v-else-if="filteredApplicants.length === 0"
      class="empty-box"
    >
      No applicants found.
    </div>

    <!-- Applicants -->
    <div
      v-else
      class="applicant-grid"
    >

      <div
        v-for="applicant in filteredApplicants"
        :key="applicant.application_id"
        class="applicant-card"
      >

        <!-- Top -->
        <div class="card-top">

          <div>

            <h3>
              {{ applicant.student_name }}
            </h3>

            <p class="student-email">
              {{ applicant.student_email }}
            </p>

          </div>

          <span
            class="status-badge"
            :class="applicant.status.toLowerCase()"
          >
            {{ applicant.status }}
          </span>

        </div>

        <!-- Details -->
        <div class="details-grid">

          <div class="detail-item">

            <label>Branch</label>

            <span>
              {{ applicant.branch }}
            </span>

          </div>

          <div class="detail-item">

            <label>CGPA</label>

            <span>
              {{ applicant.cgpa }}
            </span>

          </div>

          <div class="detail-item">

            <label>Year</label>

            <span>
              {{ applicant.year }}
            </span>

          </div>

          <div class="detail-item">

            <label>Phone</label>

            <span>
              {{ applicant.phone }}
            </span>

          </div>

          <div class="detail-item">

            <label>College</label>

            <span>
              {{ applicant.college }}
            </span>

          </div>

          <div class="detail-item">

            <label>Applied On</label>

            <span>
              {{ formatDate(applicant.application_date) }}
            </span>

          </div>

        </div>

        <!-- Skills -->
        <div class="skills-section">

          <label>Skills</label>

          <p>
            {{
              applicant.skills ||
              "No skills added"
            }}
          </p>

        </div>

        <!-- Interview -->
        <div
          v-if="applicant.interview_date"
          class="interview-box"
        >

          <strong>
            Interview:
          </strong>

          {{ formatDateTime(applicant.interview_date) }}

        </div>

        <!-- Resume -->
        <div class="resume-section">

          <a
            v-if="applicant.resume"
            :href="applicant.resume"
            target="_blank"
            class="resume-btn"
          >
            View Resume
          </a>

          <span
            v-else
            class="no-resume"
          >
            Resume not uploaded
          </span>

        </div>

        <!-- Actions -->
        <div class="actions">

          <button
            class="shortlist-btn"
            @click="updateStatus(
              applicant.application_id,
              'Shortlisted'
            )"
          >
            Shortlist
          </button>

          <button
            class="select-btn"
            @click="updateStatus(
              applicant.application_id,
              'Selected'
            )"
          >
            Select
          </button>

          <button
            class="reject-btn"
            @click="updateStatus(
              applicant.application_id,
              'Rejected'
            )"
          >
            Reject
          </button>

          <button
            class="interview-btn"
            @click="openInterviewModal(applicant)"
          >
            Interview
          </button>

        </div>

      </div>

    </div>

    <!-- Interview Modal -->
    <div
      v-if="showModal"
      class="modal-overlay"
    >

      <div class="modal-box">

        <div class="modal-header">

          <h3>
            Schedule Interview
          </h3>

          <button
            class="close-btn"
            @click="closeModal"
          >
            ✕
          </button>

        </div>

        <form @submit.prevent="scheduleInterview">

          <div class="form-group">

            <label>
              Interview Date & Time
            </label>

            <input
              type="datetime-local"
              v-model="interviewDate"
              required
            />

          </div>

          <button
            type="submit"
            class="submit-btn"
          >
            Schedule Interview
          </button>

        </form>

      </div>

    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {

  name: "ApplicantsView",

  data() {

    return {

      loading: true,

      applicants: [],

      search: "",

      statusFilter: "",

      showModal: false,

      selectedApplicationId: null,

      interviewDate: ""

    };

  },

  computed: {

    filteredApplicants() {

      return this.applicants.filter(
        (applicant) => {

          const keyword =
            this.search.toLowerCase();

          const matchesSearch =

            applicant.student_name
              .toLowerCase()
              .includes(keyword)

            ||

            applicant.branch
              .toLowerCase()
              .includes(keyword)

            ||

            (applicant.skills || "")
              .toLowerCase()
              .includes(keyword);

          const matchesStatus =

            !this.statusFilter ||

            applicant.status ===
            this.statusFilter;

          return (
            matchesSearch &&
            matchesStatus
          );

        }
      );

    }

  },

  mounted() {

    this.fetchApplicants();

  },

  methods: {

    getHeaders() {

      return {

        headers: {

          Authorization:
            `Bearer ${localStorage.getItem("token")}`

        }

      };

    },

    async fetchApplicants() {

      try {

        const driveId =
          this.$route.params.id;

        const response = await axios.get(

          `http://127.0.0.1:5000/api/company/drives/${driveId}/applicants`,

          this.getHeaders()

        );

        this.applicants =
          response.data;

      }

      catch (error) {

        console.error(error);

        alert(

          error.response?.data?.message ||

          "Failed to load applicants."

        );

      }

      finally {

        this.loading = false;

      }

    },

    formatDate(date) {

      if (!date) return "-";

      return new Date(date)
        .toLocaleDateString();

    },

    formatDateTime(date) {

      if (!date) return "-";

      return new Date(date)
        .toLocaleString();

    },

    async updateStatus(
      applicationId,
      status
    ) {

      try {

        const response =
          await axios.put(

            `http://127.0.0.1:5000/api/company/applications/${applicationId}/status`,

            {
              status
            },

            this.getHeaders()

          );

        alert(
          response.data.message
        );

        this.fetchApplicants();

      }

      catch (error) {

        console.error(error);

        alert(

          error.response?.data?.message ||

          "Failed to update status."

        );

      }

    },

    openInterviewModal(applicant) {

      this.showModal = true;

      this.selectedApplicationId =
        applicant.application_id;

    },

    closeModal() {

      this.showModal = false;

      this.interviewDate = "";

    },

    async scheduleInterview() {

      try {

        const formattedDate =
          this.interviewDate
            .replace("T", " ") + ":00";

        const response =
          await axios.put(

            `http://127.0.0.1:5000/api/company/applications/${this.selectedApplicationId}/schedule-interview`,

            {

              interview_date:
                formattedDate

            },

            this.getHeaders()

          );

        alert(
          response.data.message
        );

        this.closeModal();

        this.fetchApplicants();

      }

      catch (error) {

        console.error(error);

        alert(

          error.response?.data?.message ||

          "Failed to schedule interview."

        );

      }

    }

  }

};
</script>

<style scoped>

.applicants-page {

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

  gap: 20px;
  flex-wrap: wrap;

  margin-bottom: 30px;

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

  background:
    linear-gradient(
      135deg,
      #7c3aed,
      #dc2626
    );

  color: white;

  padding: 14px 20px;
  border-radius: 14px;

  font-weight: 700;

}

/* =========================
   FILTERS
========================= */

.filter-section {

  display: flex;
  gap: 16px;
  flex-wrap: wrap;

  margin-bottom: 30px;

}

.filter-section input,
.filter-section select {

  flex: 1;

  min-width: 220px;

  padding: 14px 16px;

  border-radius: 14px;

  border: 1px solid #dbeafe;

  outline: none;

  background: white;

}

.filter-section input:focus,
.filter-section select:focus {

  border-color: #7c3aed;

  box-shadow:
    0 0 0 4px rgba(124,58,237,0.08);

}

/* =========================
   STATES
========================= */

.loading-box,
.empty-box {

  background: white;

  padding: 50px;

  border-radius: 22px;

  text-align: center;
  font-weight: 700;

}

/* =========================
   GRID
========================= */

.applicant-grid {

  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(380px, 1fr));

  gap: 24px;

}

.applicant-card {

  background: white;

  border-radius: 24px;

  padding: 24px;

  box-shadow:
    0 15px 40px rgba(0,0,0,0.05);

}

/* =========================
   TOP
========================= */

.card-top {

  display: flex;
  justify-content: space-between;
  align-items: flex-start;

  gap: 16px;

  margin-bottom: 24px;

}

.card-top h3 {

  margin: 0;
  color: #1e1b4b;

}

.student-email {

  margin-top: 6px;
  color: #64748b;

}

.status-badge {

  padding: 8px 14px;

  border-radius: 50px;

  font-size: 12px;
  font-weight: 700;

  text-transform: uppercase;

}

.status-badge.applied {

  background: #dbeafe;
  color: #2563eb;

}

.status-badge.shortlisted {

  background: #fef3c7;
  color: #d97706;

}

.status-badge.selected {

  background: #dcfce7;
  color: #16a34a;

}

.status-badge.rejected {

  background: #fee2e2;
  color: #dc2626;

}

/* =========================
   DETAILS
========================= */

.details-grid {

  display: grid;

  grid-template-columns:
    repeat(2, 1fr);

  gap: 18px;

  margin-bottom: 20px;

}

.detail-item label {

  display: block;

  font-size: 13px;
  color: #64748b;

  margin-bottom: 6px;

}

.detail-item span {

  font-weight: 700;
  color: #334155;

}

/* =========================
   SKILLS
========================= */

.skills-section {

  margin-bottom: 20px;

}

.skills-section label {

  display: block;

  font-size: 13px;
  color: #64748b;

  margin-bottom: 8px;

}

.skills-section p {

  margin: 0;

  line-height: 1.7;
  color: #475569;

}

/* =========================
   INTERVIEW
========================= */

.interview-box {

  background:
    rgba(124,58,237,0.08);

  padding: 14px;
  border-radius: 14px;

  margin-bottom: 18px;

  color: #5b21b6;
  font-weight: 600;

}

/* =========================
   RESUME
========================= */

.resume-section {

  margin-bottom: 22px;

}

.resume-btn {

  display: inline-block;

  text-decoration: none;

  background:
    linear-gradient(
      135deg,
      #7c3aed,
      #dc2626
    );

  color: white;

  padding: 12px 18px;
  border-radius: 12px;

  font-weight: 700;

}

.no-resume {

  color: #94a3b8;

}

/* =========================
   ACTIONS
========================= */

.actions {

  display: grid;

  grid-template-columns:
    repeat(2, 1fr);

  gap: 12px;

}

.actions button {

  border: none;

  padding: 12px;

  border-radius: 12px;

  font-weight: 700;

  cursor: pointer;
  transition: 0.3s;

}

.actions button:hover {

  transform: translateY(-2px);

}

.shortlist-btn {

  background: #facc15;
  color: #111827;

}

.select-btn {

  background: #16a34a;
  color: white;

}

.reject-btn {

  background: #dc2626;
  color: white;

}

.interview-btn {

  background: #7c3aed;
  color: white;

}

/* =========================
   MODAL
========================= */

.modal-overlay {

  position: fixed;
  inset: 0;

  background: rgba(0,0,0,0.45);

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 20px;
  z-index: 999;

}

.modal-box {

  width: 100%;
  max-width: 500px;

  background: white;

  border-radius: 24px;

  padding: 30px;

}

.modal-header {

  display: flex;
  justify-content: space-between;
  align-items: center;

  margin-bottom: 24px;

}

.modal-header h3 {

  margin: 0;
  color: #1e1b4b;

}

.close-btn {

  border: none;
  background: transparent;

  font-size: 24px;
  cursor: pointer;

}

.form-group label {

  display: block;

  margin-bottom: 10px;

  font-weight: 700;

}

.form-group input {

  width: 100%;

  padding: 14px;

  border-radius: 14px;

  border: 1px solid #dbeafe;

  outline: none;

}

.form-group input:focus {

  border-color: #7c3aed;

  box-shadow:
    0 0 0 4px rgba(124,58,237,0.08);

}

.submit-btn {

  width: 100%;

  margin-top: 20px;

  border: none;

  padding: 14px;

  border-radius: 14px;

  background:
    linear-gradient(
      135deg,
      #7c3aed,
      #dc2626
    );

  color: white;

  font-weight: 700;

  cursor: pointer;

}

/* =========================
   RESPONSIVE
========================= */

@media (max-width: 768px) {

  .applicants-page {

    padding: 18px;

  }

  .page-header {

    flex-direction: column;
    align-items: flex-start;

  }

  .page-header h2 {

    font-size: 28px;

  }

  .details-grid {

    grid-template-columns: 1fr;

  }

  .actions {

    grid-template-columns: 1fr;

  }

}

</style>