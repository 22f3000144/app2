<template>
  <div class="shortlisted-students-page">

    <!-- Header -->
    <div class="page-header">

      <div>

        <h2>Shortlisted Students</h2>

        <p>
          View shortlisted and selected candidates
        </p>

      </div>

      <router-link
        to="/company/dashboard"
        class="back-btn"
      >
        ← Dashboard
      </router-link>

    </div>

    <!-- Filters -->
    <div class="filters-section">

      <!-- Search -->
      <input
        type="text"
        v-model="search"
        placeholder="Search students..."
      />

      <!-- Status -->
      <select v-model="statusFilter">

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

      <!-- Drive -->
      <select v-model="driveFilter">

        <option value="">
          All Drives
        </option>

        <option
          v-for="drive in uniqueDrives"
          :key="drive"
          :value="drive"
        >
          {{ drive }}
        </option>

      </select>

    </div>

    <!-- Loading -->
    <div
      v-if="loading"
      class="loading-box"
    >
      Loading students...
    </div>

    <!-- Empty -->
    <div
      v-else-if="filteredStudents.length === 0"
      class="empty-box"
    >
      No shortlisted students found.
    </div>

    <!-- Students -->
    <div
      v-else
      class="students-grid"
    >

      <div
        v-for="student in filteredStudents"
        :key="student.application_id"
        class="student-card"
      >

        <!-- Top -->
        <div class="student-top">

          <div>

            <h3>
              {{ student.student_name }}
            </h3>

            <p>
              {{ student.student_email }}
            </p>

          </div>

          <span
            class="status-badge"
            :class="student.status.toLowerCase()"
          >
            {{ student.status }}
          </span>

        </div>

        <!-- Job -->
        <div class="job-box">

          <label>
            Applied For
          </label>

          <h4>
            {{ student.job_title }}
          </h4>

        </div>

        <!-- Details -->
        <div class="details-grid">

          <div class="detail-item">

            <label>Branch</label>

            <span>
              {{ student.branch }}
            </span>

          </div>

          <div class="detail-item">

            <label>CGPA</label>

            <span>
              {{ student.cgpa }}
            </span>

          </div>

          <div class="detail-item">

            <label>Year</label>

            <span>
              {{ student.year }}
            </span>

          </div>

          <div class="detail-item">

            <label>Phone</label>

            <span>
              {{ student.phone }}
            </span>

          </div>

        </div>

        <!-- Skills -->
        <div class="skills-box">

          <label>
            Skills
          </label>

          <p>
            {{
              student.skills ||
              "No skills added"
            }}
          </p>

        </div>

        <!-- Interview -->
        <div
          v-if="student.interview_date"
          class="interview-box"
        >

          <strong>
            Interview:
          </strong>

          {{ formatDateTime(student.interview_date) }}

        </div>

        <!-- Resume -->
        <div class="resume-section">

          <a
            v-if="student.resume"
            :href="student.resume"
            target="_blank"
            class="resume-btn"
          >
            View Resume
          </a>

          <span
            v-else
            class="no-resume"
          >
            Resume Not Uploaded
          </span>

        </div>

      </div>

    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {

  name: "ShortlistedStudentsView",

  data() {

    return {

      loading: true,

      students: [],

      search: "",

      statusFilter: "",

      driveFilter: ""

    };

  },

  computed: {

    filteredStudents() {

      return this.students.filter(
        (student) => {

          const keyword =
            this.search.toLowerCase();

          const matchesSearch =

            student.student_name
              .toLowerCase()
              .includes(keyword)

            ||

            student.student_email
              .toLowerCase()
              .includes(keyword)

            ||

            student.branch
              .toLowerCase()
              .includes(keyword)

            ||

            (student.skills || "")
              .toLowerCase()
              .includes(keyword);

          const matchesStatus =

            !this.statusFilter ||

            student.status ===
            this.statusFilter;

          const matchesDrive =

            !this.driveFilter ||

            student.job_title ===
            this.driveFilter;

          return (

            matchesSearch &&
            matchesStatus &&
            matchesDrive

          );

        }
      );

    },

    uniqueDrives() {

      return [

        ...new Set(

          this.students.map(
            student => student.job_title
          )

        )

      ];

    }

  },

  mounted() {

    this.fetchStudents();

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

    async fetchStudents() {

      try {

        const response = await axios.get(

          "http://127.0.0.1:5000/api/company/shortlisted-students",

          this.getHeaders()

        );

        this.students =
          response.data;

      }

      catch (error) {

        console.error(error);

        alert(

          error.response?.data?.message ||

          "Failed to load shortlisted students."

        );

      }

      finally {

        this.loading = false;

      }

    },

    formatDateTime(date) {

      if (!date) return "-";

      return new Date(date)
        .toLocaleString();

    }

  }

};
</script>

<style scoped>

.shortlisted-students-page {

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

  padding: 14px 22px;

  border-radius: 14px;

  font-weight: 700;

}

/* =========================
   FILTERS
========================= */

.filters-section {

  display: flex;

  gap: 16px;

  flex-wrap: wrap;

  margin-bottom: 30px;

}

.filters-section input,
.filters-section select {

  flex: 1;

  min-width: 220px;

  padding: 14px 16px;

  border-radius: 14px;

  border: 1px solid #dbeafe;

  background: white;

  outline: none;

}

.filters-section input:focus,
.filters-section select:focus {

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

  border-radius: 24px;

  text-align: center;

  font-weight: 700;

}

/* =========================
   GRID
========================= */

.students-grid {

  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(370px, 1fr));

  gap: 24px;

}

.student-card {

  background: white;

  border-radius: 24px;

  padding: 24px;

  box-shadow:
    0 15px 40px rgba(0,0,0,0.05);

  transition: 0.3s;

}

.student-card:hover {

  transform: translateY(-5px);

}

/* =========================
   TOP
========================= */

.student-top {

  display: flex;
  justify-content: space-between;
  align-items: flex-start;

  gap: 16px;

  margin-bottom: 22px;

}

.student-top h3 {

  margin: 0;

  color: #1e1b4b;

}

.student-top p {

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

.status-badge.shortlisted {

  background: #fef3c7;
  color: #d97706;

}

.status-badge.selected {

  background: #dcfce7;
  color: #16a34a;

}

/* =========================
   JOB
========================= */

.job-box {

  background:
    rgba(124,58,237,0.08);

  padding: 16px;

  border-radius: 16px;

  margin-bottom: 22px;

}

.job-box label {

  display: block;

  font-size: 13px;

  color: #7c3aed;

  margin-bottom: 8px;

}

.job-box h4 {

  margin: 0;

  color: #312e81;

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

.skills-box {

  margin-bottom: 20px;

}

.skills-box label {

  display: block;

  font-size: 13px;

  color: #64748b;

  margin-bottom: 8px;

}

.skills-box p {

  margin: 0;

  line-height: 1.7;

  color: #475569;

}

/* =========================
   INTERVIEW
========================= */

.interview-box {

  background:
    rgba(220,38,38,0.08);

  color: #b91c1c;

  padding: 14px;

  border-radius: 14px;

  margin-bottom: 20px;

  font-weight: 600;

}

/* =========================
   RESUME
========================= */

.resume-section {

  margin-top: 10px;

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
   RESPONSIVE
========================= */

@media (max-width: 768px) {

  .shortlisted-students-page {

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

}

</style>