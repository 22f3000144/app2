<template>
  <div class="company-dashboard">

    <!-- HEADER -->
    <div class="dashboard-header">
      <div>
        <h2>Company Dashboard</h2>
        <p>
          Welcome back,
          <strong>{{ company.name }}</strong>
        </p>
      </div>

      <button class="logout-btn" @click="logout">
        Logout
      </button>
    </div>

    <!-- STATS -->
    <div class="stats-grid">
      <div class="stat-card">
        <h3>{{ stats.total_drives }}</h3>
        <p>Total Drives</p>
      </div>

      <div class="stat-card">
        <h3>{{ stats.pending_drives }}</h3>
        <p>Pending Drives</p>
      </div>

      <div class="stat-card">
        <h3>{{ stats.approved_drives }}</h3>
        <p>Approved Drives</p>
      </div>

      <div class="stat-card">
        <h3>{{ stats.total_applications }}</h3>
        <p>Total Applications</p>
      </div>
    </div>

    <!-- COMPANY PROFILE -->
    <div class="profile-card">
      <h3>Company Profile</h3>

      <div class="profile-info">
        <p><strong>Email:</strong> {{ company.email }}</p>
        <p><strong>HR Contact:</strong> {{ company.hr_contact }}</p>

        <p>
          <strong>Website:</strong>
          <a :href="company.website" target="_blank">
            {{ company.website }}
          </a>
        </p>

        <p>
          <strong>Status:</strong>
          <span v-if="company.approved" class="approved">Approved</span>
          <span v-else class="pending">Pending Approval</span>
        </p>
      </div>
    </div>

    <!-- CREATE DRIVE -->
    <div class="create-drive-card">
      <h3>Create Placement Drive</h3>

      <form @submit.prevent="createDrive">

        <div class="form-grid">

          <input v-model="drive.job_title" placeholder="Job Title" required />

          <input v-model="drive.eligible_branch" placeholder="Eligible Branch" required />

          <input type="number" step="0.1" v-model="drive.min_cgpa" placeholder="Minimum CGPA" required />

          <input type="number" v-model="drive.eligible_year" placeholder="Eligible Year" required />

          <input type="date" v-model="drive.application_deadline" required />

        </div>

        <textarea
          v-model="drive.job_description"
          placeholder="Job Description"
          rows="5"
          required
        ></textarea>

        <button type="submit">Create Drive</button>
      </form>
    </div>

    <!-- DRIVES TABLE -->
    <div class="drives-card">
      <h3>Your Placement Drives</h3>

      <div v-if="drives.length === 0" class="empty-state">
        No placement drives created yet.
      </div>

      <table v-else>
        <thead>
          <tr>
            <th>ID</th>
            <th>Job Title</th>
            <th>Branch</th>
            <th>CGPA</th>
            <th>Year</th>
            <th>Deadline</th>
            <th>Status</th>
            <th>Applicants</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="drive in drives" :key="drive.id">
            <td>{{ drive.id }}</td>
            <td>{{ drive.job_title }}</td>
            <td>{{ drive.eligible_branch }}</td>
            <td>{{ drive.min_cgpa }}</td>
            <td>{{ drive.eligible_year }}</td>
            <td>{{ formatDate(drive.application_deadline) }}</td>

            <td>
              <span v-if="drive.status === 'approved'" class="approved">Approved</span>
              <span v-else-if="drive.status === 'pending' || !drive.status" class="pending">Pending</span>
              <span v-else class="rejected">Rejected</span>
            </td>

            <td>{{ drive.total_applicants || 0 }}</td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CompanyDashboardView",

  data() {
    return {
      company: {},

      stats: {
        total_drives: 0,
        pending_drives: 0,
        approved_drives: 0,
        total_applications: 0
      },

      drives: [],

      drive: {
        job_title: "",
        job_description: "",
        eligible_branch: "",
        min_cgpa: "",
        eligible_year: "",
        application_deadline: ""
      }
    };
  },

  methods: {

    getToken() {
      return localStorage.getItem("token");
    },

    formatDate(date) {
      return date ? new Date(date).toLocaleDateString() : "";
    },

    async fetchDashboard() {
      try {
        const res = await axios.get(
          "http://127.0.0.1:5000/api/company/dashboard",
          {
            headers: {
              Authorization: `Bearer ${this.getToken()}`
            }
          }
        );

        this.company = res.data.company;
        this.stats = res.data.stats;

      } catch (err) {
        console.error("Dashboard Error:", err.response?.data || err);
      }
    },

    async fetchDrives() {
      try {
        const res = await axios.get(
          "http://127.0.0.1:5000/api/company/drives",
          {
            headers: {
              Authorization: `Bearer ${this.getToken()}`
            }
          }
        );

        this.drives = res.data;

      } catch (err) {
        console.error("Drives Error:", err.response?.data || err);
      }
    },

    async createDrive() {
      try {
        await axios.post(
          "http://127.0.0.1:5000/api/company/drive/create",
          this.drive,
          {
            headers: {
              Authorization: `Bearer ${this.getToken()}`
            }
          }
        );

        alert("Drive created successfully");

        this.drive = {
          job_title: "",
          job_description: "",
          eligible_branch: "",
          min_cgpa: "",
          eligible_year: "",
          application_deadline: ""
        };

        this.fetchDrives();
        this.fetchDashboard();

      } catch (err) {
        console.error("Create Drive Error:", err.response?.data || err);
        alert(err.response?.data?.message || "Error creating drive");
      }
    },

    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    }
  },

  mounted() {
    this.fetchDashboard();
    this.fetchDrives();
  }
};
</script>

<style scoped>
.company-dashboard {
  padding: 30px;
  background: #f4f7fb;
  min-height: 100vh;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.logout-btn {
  background: #ef4444;
  color: white;
  border: none;
  padding: 10px 18px;
  border-radius: 8px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
}

.profile-card,
.create-drive-card,
.drives-card {
  background: white;
  padding: 25px;
  border-radius: 14px;
  margin-bottom: 25px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 15px;
}

input,
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

button {
  background: #2563eb;
  color: white;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
}

.approved { color: green; font-weight: bold; }
.pending { color: orange; font-weight: bold; }
.rejected { color: red; font-weight: bold; }

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  border-bottom: 1px solid #eee;
}

.empty-state {
  text-align: center;
  padding: 20px;
  color: gray;
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style>