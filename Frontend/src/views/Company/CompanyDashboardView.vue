<template>
  <div class="company-dashboard">

    <!-- ======================================
    HEADER
    ======================================= -->

    <div class="dashboard-header">

      <div>
        <h2>Company Dashboard</h2>
        <p>
          Welcome back,
          <strong>{{ company.name }}</strong>
        </p>
      </div>

      <button
        class="logout-btn"
        @click="logout"
      >
        Logout
      </button>

    </div>


    <!-- ======================================
    STATISTICS
    ======================================= -->

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


    <!-- ======================================
    COMPANY INFO
    ======================================= -->

    <div class="profile-card">

      <h3>Company Profile</h3>

      <div class="profile-info">

        <p>
          <strong>Email:</strong>
          {{ company.email }}
        </p>

        <p>
          <strong>HR Contact:</strong>
          {{ company.hr_contact }}
        </p>

        <p>
          <strong>Website:</strong>
          <a
            :href="company.website"
            target="_blank"
          >
            {{ company.website }}
          </a>
        </p>

        <p>
          <strong>Status:</strong>

          <span
            class="approved"
            v-if="company.approved"
          >
            Approved
          </span>

          <span
            class="pending"
            v-else
          >
            Pending Approval
          </span>

        </p>

      </div>

    </div>


    <!-- ======================================
    CREATE DRIVE
    ======================================= -->

    <div class="create-drive-card">

      <h3>Create Placement Drive</h3>

      <form @submit.prevent="createDrive">

        <div class="form-grid">

          <input
            type="text"
            v-model="drive.job_title"
            placeholder="Job Title"
            required
          />

          <input
            type="text"
            v-model="drive.branch"
            placeholder="Eligible Branch"
            required
          />

          <input
            type="number"
            step="0.1"
            v-model="drive.cgpa"
            placeholder="Minimum CGPA"
            required
          />

          <input
            type="date"
            v-model="drive.deadline"
            required
          />

        </div>

        <textarea
          v-model="drive.description"
          placeholder="Job Description"
          rows="5"
          required
        ></textarea>

        <button type="submit">
          Create Drive
        </button>

      </form>

    </div>


    <!-- ======================================
    DRIVES TABLE
    ======================================= -->

    <div class="drives-card">

      <h3>Your Placement Drives</h3>

      <div
        v-if="drives.length === 0"
        class="empty-state"
      >
        No placement drives created yet.
      </div>

      <table v-else>

        <thead>

          <tr>
            <th>ID</th>
            <th>Job Title</th>
            <th>Branch</th>
            <th>CGPA</th>
            <th>Deadline</th>
            <th>Status</th>
            <th>Applicants</th>
          </tr>

        </thead>

        <tbody>

          <tr
            v-for="drive in drives"
            :key="drive.id"
          >

            <td>{{ drive.id }}</td>

            <td>{{ drive.job_title }}</td>

            <td>{{ drive.branch }}</td>

            <td>{{ drive.cgpa }}</td>

            <td>{{ drive.deadline }}</td>

            <td>

              <span
                class="approved"
                v-if="drive.status === 'approved'"
              >
                Approved
              </span>

              <span
                class="pending"
                v-else-if="drive.status === 'pending'"
              >
                Pending
              </span>

              <span
                class="rejected"
                v-else
              >
                Rejected
              </span>

            </td>

            <td>
              {{ drive.total_applicants || 0 }}
            </td>

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
        description: "",
        branch: "",
        cgpa: "",
        deadline: ""
      }

    };
  },

  methods: {

    // ======================================
    // GET AUTH TOKEN
    // ======================================

    getToken() {

      return localStorage.getItem("token");

    },


    // ======================================
    // LOAD DASHBOARD DATA
    // ======================================
// profile
    async fetchDashboard() {

      try {

        const response = await axios.get(
          "http://127.0.0.1:5000/api/company/dashboard",
          {
            headers: {
              Authorization: `Bearer ${this.getToken()}`
            }
          }
        );

        this.company = response.data.company;
        this.stats = response.data.stats;

      }

      catch (error) {

        console.error(error);

      }

    },


    // ======================================
    // LOAD COMPANY DRIVES
    // ======================================

    async fetchDrives() {

      try {

        const response = await axios.get(
          "http://127.0.0.1:5000/api/company/drives",
          {
            headers: {
              Authorization: `Bearer ${this.getToken()}`
            }
          }
        );

        this.drives = response.data;

      }

      catch (error) {

        console.error(error);

      }

    },


    // ======================================
    // CREATE DRIVE
    // ======================================

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

        alert("Placement drive created successfully.");

        this.drive = {
          job_title: "",
          description: "",
          branch: "",
          cgpa: "",
          deadline: ""
        };

        this.fetchDrives();
        this.fetchDashboard();

      }

      catch (error) {

        console.error(error);

        alert(
          error.response?.data?.message ||
          "Failed to create drive."
        );

      }

    },


    // ======================================
    // LOGOUT
    // ======================================

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


/* ======================================
HEADER
====================================== */

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.dashboard-header h2 {
  margin: 0;
  color: #1e293b;
}

.dashboard-header p {
  margin-top: 6px;
  color: #64748b;
}

.logout-btn {
  background: #ef4444;
  color: white;
  border: none;
  padding: 10px 18px;
  border-radius: 8px;
  cursor: pointer;
}


/* ======================================
STATS
====================================== */

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  padding: 25px;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

.stat-card h3 {
  font-size: 32px;
  margin-bottom: 10px;
  color: #2563eb;
}


/* ======================================
CARDS
====================================== */

.profile-card,
.create-drive-card,
.drives-card {

  background: white;
  padding: 25px;
  border-radius: 14px;
  margin-bottom: 30px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);

}

.profile-info p {
  margin-bottom: 10px;
}


/* ======================================
FORM
====================================== */

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 15px;
  margin-bottom: 15px;
}

input,
textarea {

  width: 100%;
  padding: 12px;
  border: 1px solid #dbe2ea;
  border-radius: 8px;
  outline: none;
  font-size: 14px;

}

textarea {
  margin-bottom: 15px;
}

button {

  background: #2563eb;
  color: white;
  border: none;
  padding: 12px 18px;
  border-radius: 8px;
  cursor: pointer;

}


/* ======================================
TABLE
====================================== */

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #eff6ff;
}

th,
td {
  padding: 14px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}


/* ======================================
STATUS
====================================== */

.approved {
  color: #16a34a;
  font-weight: bold;
}

.pending {
  color: #f59e0b;
  font-weight: bold;
}
/* api */
.rejected {
  color: #dc2626;
  font-weight: bold;
}


/* ======================================
EMPTY STATE
====================================== */

.empty-state {
  padding: 20px;
  text-align: center;
  color: #64748b;
}


/* ======================================
RESPONSIVE
====================================== */

@media (max-width: 768px) {

  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  table {
    display: block;
    overflow-x: auto;
  }

}

</style>