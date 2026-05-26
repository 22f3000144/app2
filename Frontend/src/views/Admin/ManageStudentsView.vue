<template>
  <div class="manage-students-page">

    <!-- Header -->
    <div class="page-header">

      <div>
        <h2>Manage Students</h2>
        <p>View and manage registered students</p>
      </div>

      <div class="search-box">
        <input
          type="text"
          placeholder="Search students..."
          v-model="search"
        />
      </div>

    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading-box">
      Loading Students...
    </div>

    <!-- Content -->
    <div v-else>

      <!-- Empty -->
      <div
        v-if="filteredStudents.length === 0"
        class="empty-box"
      >

        <i class="bi bi-people"></i>

        <h4>No Students Found</h4>

        <p>
          Registered students will appear here.
        </p>

      </div>

      <!-- Students Table -->
      <div
        v-else
        class="table-responsive student-table-wrapper"
      >

        <table class="table student-table">

          <thead>
            <tr>
              <th>ID</th>
              <th>Student</th>
              <th>Email</th>
              <th>Phone</th>
              <th>College</th>
              <th>Branch</th>
              <th>Skills</th>
              <th>CGPA</th>
              <th>Year</th>
              <th>Status</th>
              <th>Resume</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="student in filteredStudents"
              :key="student.id"
            >

              <td>{{ student.id }}</td>

              <!-- Student Info -->
              <td>

                <div class="student-info">

                  <div class="student-avatar">
                    {{ student.name?.charAt(0) }}
                  </div>

                  <div>

                    <h6>{{ student.name }}</h6>

                    <small>
                      Registered Student
                    </small>

                  </div>

                </div>

              </td>

              <td>{{ student.email }}</td>

              <td>{{ student.phone || 'N/A' }}</td>

              <td>{{ student.college || 'N/A' }}</td>

              <td>{{ student.branch }}</td>

              <td>{{ student.skills || 'N/A' }}</td>

              <td>{{ student.cgpa }}</td>

              <td>{{ student.year }}</td>

              <!-- Status -->
              <td>

                <span
                  v-if="student.active"
                  class="status-badge active"
                >
                  Active
                </span>

                <span
                  v-else
                  class="status-badge blocked"
                >
                  Blocked
                </span>

              </td>

              <!-- Resume -->
              <td>

                <a
                  v-if="student.resume"
                  :href="student.resume"
                  target="_blank"
                  class="resume-link"
                >
                  View Resume
                </a>

                <span v-else class="no-resume">
                  No Resume
                </span>

              </td>

              <!-- Actions -->
              <td>

                <div class="action-buttons">

                  <button
                    class="view-btn"
                    @click="viewStudent(student)"
                  >
                    View
                  </button>

                  <button
                    v-if="student.active"
                    class="block-btn"
                    @click="blockStudent(student.id)"
                  >
                    Block
                  </button>

                  <span
                    v-else
                    class="blocked-text"
                  >
                    Student Blocked
                  </span>

                  <button
                    class="delete-btn"
                    @click="deleteStudent(student.id)"
                  >
                    Delete
                  </button>

                </div>

              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

    <!-- Student Modal -->
    <div
      v-if="selectedStudent"
      class="modal-overlay"
    >

      <div class="student-modal">

        <div class="modal-header">

          <h4>Student Details</h4>

          <button
            class="close-btn"
            @click="selectedStudent = null"
          >
            ×
          </button>

        </div>

        <div class="modal-body">

          <div class="profile-circle">
            {{ selectedStudent.name?.charAt(0) }}
          </div>

          <h3>{{ selectedStudent.name }}</h3>

          <p>{{ selectedStudent.email }}</p>

          <div class="details-grid">

            <div class="detail-card">
              <h6>Phone</h6>
              <p>{{ selectedStudent.phone || 'N/A' }}</p>
            </div>

            <div class="detail-card">
              <h6>College</h6>
              <p>{{ selectedStudent.college || 'N/A' }}</p>
            </div>

            <div class="detail-card">
              <h6>Branch</h6>
              <p>{{ selectedStudent.branch }}</p>
            </div>

            <div class="detail-card">
              <h6>Skills</h6>
              <p>{{ selectedStudent.skills || 'N/A' }}</p>
            </div>

            <div class="detail-card">
              <h6>CGPA</h6>
              <p>{{ selectedStudent.cgpa }}</p>
            </div>

            <div class="detail-card">
              <h6>Year</h6>
              <p>{{ selectedStudent.year }}</p>
            </div>

            <div class="detail-card">
              <h6>Status</h6>
              <p>
                {{ selectedStudent.active ? 'Active' : 'Blocked' }}
              </p>
            </div>

            <div class="detail-card">
              <h6>Resume</h6>

              <p v-if="selectedStudent.resume">
                <a
                  :href="selectedStudent.resume"
                  target="_blank"
                  class="resume-link"
                >
                  Open Resume
                </a>
              </p>

              <p v-else>
                No Resume
              </p>

            </div>

          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import axios from 'axios'
import { computed, onMounted, ref } from 'vue'

const loading = ref(true)

const search = ref('')

const students = ref([])

const selectedStudent = ref(null)

const fetchStudents = async () => {

  try {

    const token = localStorage.getItem('token')

    const response = await axios.get(
      'http://127.0.0.1:5000/api/admin/students',
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    students.value = response.data || []

  } catch (error) {

    console.log(error)

  } finally {

    loading.value = false
  }
}

onMounted(() => {
  fetchStudents()
})

const filteredStudents = computed(() => {

  return students.value.filter((student) => {

    return (

      student.name
        ?.toLowerCase()
        .includes(search.value.toLowerCase()) ||

      student.email
        ?.toLowerCase()
        .includes(search.value.toLowerCase()) ||

      student.branch
        ?.toLowerCase()
        .includes(search.value.toLowerCase()) ||

      student.college
        ?.toLowerCase()
        .includes(search.value.toLowerCase()) ||

      student.skills
        ?.toLowerCase()
        .includes(search.value.toLowerCase()) ||

      student.phone
        ?.toLowerCase()
        .includes(search.value.toLowerCase())
    )
  })
})

const viewStudent = (student) => {

  selectedStudent.value = student
}

const blockStudent = async (studentId) => {

  const confirmBlock = confirm(
    'Are you sure you want to block this student?'
  )

  if (!confirmBlock) return

  try {

    const token = localStorage.getItem('token')

    await axios.put(
      `http://127.0.0.1:5000/api/admin/student/block/${studentId}`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    alert('Student Blocked')

    fetchStudents()

  } catch (error) {

    console.log(error)

    alert('Block Failed')
  }
}

const deleteStudent = async (studentId) => {

  const confirmDelete = confirm(
    'Are you sure you want to delete this student?'
  )

  if (!confirmDelete) return

  try {

    const token = localStorage.getItem('token')

    await axios.delete(
      `http://127.0.0.1:5000/api/admin/student/${studentId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    alert('Student Deleted')

    fetchStudents()

  } catch (error) {

    console.log(error)

    alert('Delete Failed')
  }
}
</script>

<style scoped>
.manage-students-page {
  min-height: 100vh;
  background: #f1f5f9;
  padding: 25px;
}

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  gap: 20px;
  flex-wrap: wrap;

  margin-bottom: 30px;
}

.page-header h2 {
  font-weight: 700;
  margin-bottom: 5px;
}

.page-header p {
  color: #64748b;
}

/* Search */
.search-box input {
  width: 280px;

  border: none;
  outline: none;

  background: white;

  padding: 12px 16px;

  border-radius: 12px;

  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

/* Table */
.student-table-wrapper {
  background: white;

  border-radius: 18px;

  padding: 20px;

  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.student-table {
  margin-bottom: 0;
  min-width: 1400px;
}

.student-table thead {
  background: #0f172a;
  color: white;
}

.student-table th,
.student-table td {
  vertical-align: middle;
  padding: 16px;
}

/* Student Info */
.student-info {
  display: flex;
  align-items: center;
  gap: 14px;
}

.student-avatar {
  width: 45px;
  height: 45px;

  border-radius: 50%;

  background: #2563eb;
  color: white;

  display: flex;
  align-items: center;
  justify-content: center;

  font-weight: 700;
  font-size: 18px;
}

.student-info h6 {
  margin-bottom: 2px;
  font-weight: 600;
}

.student-info small {
  color: #64748b;
}

/* Resume */
.resume-link {
  text-decoration: none;
  color: #2563eb;
  font-weight: 600;
}

.no-resume {
  color: #94a3b8;
}

/* Status */
.status-badge {
  padding: 6px 14px;

  border-radius: 30px;

  font-size: 13px;
  font-weight: 600;
}

.active {
  background: #dcfce7;
  color: #166534;
}

.blocked {
  background: #fee2e2;
  color: #991b1b;
}

/* Buttons */
.action-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.view-btn,
.block-btn,
.delete-btn {
  border: none;

  padding: 8px 14px;

  border-radius: 10px;

  color: white;

  font-size: 14px;
  font-weight: 600;

  transition: 0.3s;
}

.view-btn {
  background: #2563eb;
}

.block-btn {
  background: #ea580c;
}

.delete-btn {
  background: #dc2626;
}

.view-btn:hover,
.block-btn:hover,
.delete-btn:hover {
  transform: translateY(-2px);
}

/* Empty */
.empty-box {
  background: white;

  border-radius: 18px;

  padding: 80px 20px;

  text-align: center;

  color: #64748b;
}

.empty-box i {
  font-size: 65px;
  margin-bottom: 15px;
}

/* Loading */
.loading-box {
  background: white;

  border-radius: 18px;

  padding: 80px;

  text-align: center;

  font-size: 20px;
  font-weight: 600;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;

  background: rgba(0,0,0,0.4);

  display: flex;
  align-items: center;
  justify-content: center;

  z-index: 1000;
}

.student-modal {
  width: 100%;
  max-width: 650px;

  background: white;

  border-radius: 20px;

  padding: 25px;

  animation: popup 0.3s ease;
}

@keyframes popup {

  from {
    transform: scale(0.9);
    opacity: 0;
  }

  to {
    transform: scale(1);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  margin-bottom: 25px;
}

.close-btn {
  border: none;
  background: transparent;

  font-size: 28px;

  cursor: pointer;
}

.modal-body {
  text-align: center;
}

.profile-circle {
  width: 90px;
  height: 90px;

  border-radius: 50%;

  background: #2563eb;
  color: white;

  margin: auto;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 32px;
  font-weight: 700;

  margin-bottom: 18px;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));

  gap: 18px;

  margin-top: 30px;
}

.detail-card {
  background: #f8fafc;

  border-radius: 14px;

  padding: 18px;
}

.detail-card h6 {
  color: #64748b;
  margin-bottom: 10px;
}

/* Responsive */
@media (max-width: 992px) {

  .student-table {
    min-width: 1400px;
  }
}

@media (max-width: 576px) {

  .manage-students-page {
    padding: 15px;
  }

  .search-box input {
    width: 100%;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .student-modal {
    margin: 15px;
  }
}

.blocked-text {
  color: #dc2626;
  font-weight: 700;
  font-size: 14px;
}
</style>