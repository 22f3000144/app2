<template>
  <div class="manage-drives-page">

    <!-- Header -->
    <div class="page-header">

      <div>
        <h2>Manage Placement Drives</h2>

        <p>
          View, edit, and manage all recruitment drives
        </p>
      </div>

      <router-link
        to="/company/create-drive"
        class="create-btn"
      >
        + Create Drive
      </router-link>

    </div>

    <!-- Search -->
    <div class="search-section">

      <input
        type="text"
        v-model="search"
        placeholder="Search drives by title or branch..."
      />

    </div>

    <!-- Loading -->
    <div
      v-if="loading"
      class="loading-box"
    >
      Loading drives...
    </div>

    <!-- Empty -->
    <div
      v-else-if="filteredDrives.length === 0"
      class="empty-box"
    >
      No placement drives found.
    </div>

    <!-- Drives Grid -->
    <div
      v-else
      class="drives-grid"
    >

      <div
        v-for="drive in filteredDrives"
        :key="drive.id"
        class="drive-card"
      >

        <!-- Top -->
        <div class="card-top">

          <div>

            <h3>
              {{ drive.job_title }}
            </h3>

            <span
              class="status-badge"
              :class="drive.status"
            >
              {{ drive.status }}
            </span>

          </div>

          <div class="applicant-box">
            {{ drive.total_applicants }}
            <span>Applicants</span>
          </div>

        </div>

        <!-- Description -->
        <p class="description">
          {{ drive.job_description }}
        </p>

        <!-- Details -->
        <div class="details-grid">

          <div class="detail-item">
            <label>Branch</label>
            <span>
              {{ drive.required_branch }}
            </span>
          </div>

          <div class="detail-item">
            <label>Minimum CGPA</label>
            <span>
              {{ drive.min_cgpa }}
            </span>
          </div>

          <div class="detail-item">
            <label>Passing Year</label>
            <span>
              {{ drive.passing_year }}
            </span>
          </div>

          <div class="detail-item">
            <label>Deadline</label>
            <span>
              {{ formatDate(drive.application_deadline) }}
            </span>
          </div>

        </div>

        <!-- Actions -->
        <div class="actions">

          <button
            class="view-btn"
            @click="viewApplicants(drive.id)"
          >
            Applicants
          </button>

          <button
            class="edit-btn"
            @click="openEditModal(drive)"
          >
            Edit
          </button>

          <button
            class="delete-btn"
            @click="deleteDrive(drive.id)"
          >
            Delete
          </button>

        </div>

      </div>

    </div>

    <!-- Edit Modal -->
    <div
      v-if="showModal"
      class="modal-overlay"
    >

      <div class="modal-box">

        <div class="modal-header">

          <h3>Edit Placement Drive</h3>

          <button
            class="close-btn"
            @click="closeModal"
          >
            ✕
          </button>

        </div>

        <form @submit.prevent="updateDrive">

          <!-- Job Title -->
          <div class="form-group">

            <label>Job Title</label>

            <input
              type="text"
              v-model="form.job_title"
              required
            />

          </div>

          <!-- Description -->
          <div class="form-group">

            <label>Job Description</label>

            <textarea
              rows="5"
              v-model="form.job_description"
              required
            ></textarea>

          </div>

          <!-- Grid -->
          <div class="form-grid">

            <div class="form-group">

              <label>Required Branch</label>

              <input
                type="text"
                v-model="form.required_branch"
                required
              />

            </div>

            <div class="form-group">

              <label>Minimum CGPA</label>

              <input
                type="number"
                step="0.1"
                v-model="form.min_cgpa"
                required
              />

            </div>

            <div class="form-group">

              <label>Passing Year</label>

              <input
                type="number"
                v-model="form.passing_year"
                required
              />

            </div>

            <div class="form-group">

              <label>Application Deadline</label>

              <input
                type="date"
                v-model="form.application_deadline"
                required
              />

            </div>

          </div>

          <button
            type="submit"
            class="submit-btn"
            :disabled="updating"
          >

            <span v-if="updating">
              Updating...
            </span>

            <span v-else>
              Update Drive
            </span>

          </button>

        </form>

      </div>

    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {

  name: "ManageDriveView",

  data() {

    return {

      loading: true,

      updating: false,

      search: "",

      drives: [],

      showModal: false,

      selectedDriveId: null,

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

  computed: {

    filteredDrives() {

      return this.drives.filter((drive) => {

        const keyword = this.search.toLowerCase();

        return (

          drive.job_title
            .toLowerCase()
            .includes(keyword)

          ||

          drive.required_branch
            .toLowerCase()
            .includes(keyword)

        );

      });

    }

  },

  mounted() {

    this.fetchDrives();

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

    async fetchDrives() {

      try {

        const response = await axios.get(

          "http://127.0.0.1:5000/api/company/drives",

          this.getHeaders()

        );

        this.drives = response.data;

      }

      catch (error) {

        console.error(error);

        alert(

          error.response?.data?.message ||

          "Failed to load drives."

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

    openEditModal(drive) {

      this.showModal = true;

      this.selectedDriveId = drive.id;

      this.form = {

        job_title:
          drive.job_title,

        job_description:
          drive.job_description,

        required_branch:
          drive.required_branch,

        min_cgpa:
          drive.min_cgpa,

        passing_year:
          drive.passing_year,

        application_deadline:
          drive.application_deadline

      };

    },

    closeModal() {

      this.showModal = false;

      this.selectedDriveId = null;

    },

    async updateDrive() {

      try {

        this.updating = true;

        const response = await axios.put(

          `http://127.0.0.1:5000/api/company/drives/${this.selectedDriveId}`,

          this.form,

          this.getHeaders()

        );

        alert(
          response.data.message
        );

        this.closeModal();

        this.fetchDrives();

      }

      catch (error) {

        console.error(error);

        alert(

          error.response?.data?.message ||

          "Failed to update drive."

        );

      }

      finally {

        this.updating = false;

      }

    },

    async deleteDrive(id) {

      const confirmDelete = confirm(
        "Are you sure you want to delete this drive?"
      );

      if (!confirmDelete) return;

      try {

        const response = await axios.delete(

          `http://127.0.0.1:5000/api/company/drives/${id}`,

          this.getHeaders()

        );

        alert(
          response.data.message
        );

        this.fetchDrives();

      }

      catch (error) {

        console.error(error);

        alert(

          error.response?.data?.message ||

          "Failed to delete drive."

        );

      }

    },

    viewApplicants(id) {

      this.$router.push(
        `/company/applicants/${id}`
      );

    }

  }

};
</script>

<style scoped>

.manage-drives-page {

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

.create-btn {

  text-decoration: none;

  background:
    linear-gradient(
      135deg,
      #7c3aed,
      #dc2626
    );

  color: white;

  padding: 14px 22px;
  border-radius: 14px;

  font-weight: 700;

  transition: 0.3s;

}

.create-btn:hover {

  transform: translateY(-2px);

}

/* =========================
   SEARCH
========================= */

.search-section {

  margin-bottom: 30px;

}

.search-section input {

  width: 100%;
  max-width: 500px;

  padding: 14px 18px;

  border-radius: 14px;
  border: 1px solid #dbeafe;

  outline: none;
  font-size: 15px;

  background: white;

}

.search-section input:focus {

  border-color: #7c3aed;

  box-shadow:
    0 0 0 4px rgba(124, 58, 237, 0.08);

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

.drives-grid {

  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(350px, 1fr));

  gap: 25px;

}

.drive-card {

  background: white;

  border-radius: 24px;

  padding: 24px;

  box-shadow:
    0 15px 40px rgba(0,0,0,0.05);

  transition: 0.3s;

}

.drive-card:hover {

  transform: translateY(-6px);

}

.card-top {

  display: flex;
  justify-content: space-between;
  align-items: flex-start;

  gap: 16px;

  margin-bottom: 20px;

}

.card-top h3 {

  margin: 0;
  color: #1e1b4b;

}

.status-badge {

  display: inline-block;

  margin-top: 10px;

  padding: 6px 14px;

  border-radius: 50px;

  font-size: 12px;
  font-weight: 700;

  text-transform: uppercase;

}

.status-badge.pending {

  background: #fff7ed;
  color: #c2410c;

}

.status-badge.approved {

  background: #ecfdf5;
  color: #059669;

}

.status-badge.closed {

  background: #f1f5f9;
  color: #475569;

}

.applicant-box {

  min-width: 90px;

  text-align: center;

  background:
    linear-gradient(
      135deg,
      #7c3aed,
      #dc2626
    );

  color: white;

  padding: 14px;
  border-radius: 16px;

  font-size: 24px;
  font-weight: bold;

}

.applicant-box span {

  display: block;

  font-size: 12px;
  margin-top: 4px;

}

.description {

  color: #64748b;
  line-height: 1.7;

  margin-bottom: 22px;

}

.details-grid {

  display: grid;

  grid-template-columns:
    repeat(2, 1fr);

  gap: 18px;

  margin-bottom: 25px;

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
   ACTIONS
========================= */

.actions {

  display: flex;
  gap: 12px;
  flex-wrap: wrap;

}

.actions button {

  flex: 1;

  border: none;

  padding: 12px 16px;

  border-radius: 12px;

  cursor: pointer;

  font-weight: 700;
  transition: 0.3s;

}

.view-btn {

  background: #7c3aed;
  color: white;

}

.edit-btn {

  background: #facc15;
  color: #111827;

}

.delete-btn {

  background: #dc2626;
  color: white;

}

.actions button:hover {

  transform: translateY(-2px);

}

/* =========================
   MODAL
========================= */

.modal-overlay {

  position: fixed;
  inset: 0;

  background: rgba(0,0,0,0.45);

  display: flex;
  justify-content: center;
  align-items: center;

  padding: 20px;
  z-index: 999;

}

.modal-box {

  width: 100%;
  max-width: 800px;

  background: white;

  border-radius: 26px;

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

/* =========================
   FORM
========================= */

.form-group {

  margin-bottom: 22px;

}

.form-group label {

  display: block;

  margin-bottom: 10px;

  font-weight: 700;
  color: #334155;

}

.form-group input,
.form-group textarea {

  width: 100%;

  padding: 14px 16px;

  border-radius: 14px;

  border: 1px solid #dbeafe;

  outline: none;

  background: #fafafa;

}

.form-group input:focus,
.form-group textarea:focus {

  border-color: #7c3aed;

  box-shadow:
    0 0 0 4px rgba(124, 58, 237, 0.08);

  background: white;

}

.form-grid {

  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(220px, 1fr));

  gap: 18px;

}

.submit-btn {

  width: 100%;

  border: none;

  padding: 15px;

  border-radius: 14px;

  background:
    linear-gradient(
      135deg,
      #7c3aed,
      #dc2626
    );

  color: white;

  font-size: 15px;
  font-weight: 700;

  cursor: pointer;

  margin-top: 10px;

}

/* =========================
   RESPONSIVE
========================= */

@media (max-width: 768px) {

  .manage-drives-page {

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

    flex-direction: column;

  }

  .actions button {

    width: 100%;

  }

}

</style>