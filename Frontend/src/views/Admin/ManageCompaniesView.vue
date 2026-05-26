<template>
  <div class="manage-companies-page">

    <!-- Header -->
    <div class="page-header">

      <div>
        <h2>Manage Companies</h2>
        <p>Approve, reject and manage registered companies</p>
      </div>

      <div class="search-box">
        <input
          type="text"
          placeholder="Search company..."
          v-model="search"
        />
      </div>

    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading-box">
      Loading Companies...
    </div>

    <!-- Content -->
    <div v-else>

      <!-- Empty -->
      <div
        v-if="filteredCompanies.length === 0"
        class="empty-box"
      >
        <i class="bi bi-buildings"></i>

        <h4>No Companies Found</h4>

        <p>
          Registered companies will appear here.
        </p>
      </div>

      <!-- Companies Table -->
      <div
        v-else
        class="table-responsive company-table-wrapper"
      >

        <table class="table company-table">

          <thead>
            <tr>
              <th>Company</th>
              <th>HR Contact</th>
              <th>Email</th>
              <th>Website</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="company in filteredCompanies"
              :key="company.id"
            >

              <td>
                <div class="company-info">

                  <div class="company-logo">
                    {{ company.company_name?.charAt(0) }}
                  </div>

                  <div>
                    <h6>{{ company.company_name }}</h6>

                    <small>
                      Registered Company
                    </small>
                  </div>

                </div>
              </td>

              <td>
                {{ company.hr_contact }}
              </td>

              <td>
                {{ company.email }}
              </td>

              <td>
                <a
                  :href="company.website"
                  target="_blank"
                  class="website-link"
                >
                  Visit
                </a>
              </td>

              <!-- Status -->
              <td>

                <span
                  v-if="!company.active"
                  class="status-badge deactivated"
                >
                  Deactivated
                </span>

                <span
                  v-else-if="company.approved"
                  class="status-badge approved"
                >
                  Approved
                </span>

                <span
                  v-else
                  class="status-badge pending"
                >
                  Pending
                </span>

              </td>

              <!-- Actions -->
              <td>

                <div class="action-buttons">

                  <!-- Approve -->
                  <button
                    v-if="!company.approved && company.active"
                    class="approve-btn"
                    @click="approveCompany(company.id)"
                  >
                    Approve
                  </button>

                  <!-- Reject -->
                  <button
                    v-if="company.approved && company.active"
                    class="reject-btn"
                    @click="rejectCompany(company.id)"
                  >
                    Reject
                  </button>

                  <!-- Deactivate -->
                  <button
                    v-if="company.active"
                    class="delete-btn"
                    @click="deleteCompany(company.id)"
                  >
                    Deactivate
                  </button>

                  <!-- Already Deactivated -->
                  <span
                    v-if="!company.active"
                    class="deactivated-text"
                  >
                    Company Disabled
                  </span>

                </div>

              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

  </div>
</template>

<script setup>
import axios from 'axios'
import { computed, onMounted, ref } from 'vue'

const loading = ref(true)

const search = ref('')

const companies = ref([])

const fetchCompanies = async () => {

  try {

    const token = localStorage.getItem('token')

    const response = await axios.get(
      'http://127.0.0.1:5000/api/admin/companies',
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    companies.value = response.data || []

  } catch (error) {

    console.log(error)

  } finally {

    loading.value = false
  }
}

onMounted(() => {
  fetchCompanies()
})

const filteredCompanies = computed(() => {

  return companies.value.filter((company) => {

    return (

      company.company_name
        ?.toLowerCase()
        .includes(search.value.toLowerCase()) ||

      company.email
        ?.toLowerCase()
        .includes(search.value.toLowerCase())
    )
  })
})

const approveCompany = async (companyId) => {

  try {

    const token = localStorage.getItem('token')

    await axios.put(
      `http://127.0.0.1:5000/api/admin/company/approve/${companyId}`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    alert('Company Approved')

    fetchCompanies()

  } catch (error) {

    console.log(error)

    alert('Approval Failed')
  }
}

const rejectCompany = async (companyId) => {

  try {

    const token = localStorage.getItem('token')

    await axios.put(
      `http://127.0.0.1:5000/api/admin/company/reject/${companyId}`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    alert('Company Rejected')

    fetchCompanies()

  } catch (error) {

    console.log(error)

    alert('Reject Failed')
  }
}

const deleteCompany = async (companyId) => {

  const confirmDelete = confirm(
    'Are you sure you want to deactivate this company?'
  )

  if (!confirmDelete) return

  try {

    const token = localStorage.getItem('token')

    await axios.put(
      `http://127.0.0.1:5000/api/admin/company/deactivate/${companyId}`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    alert('Company Deactivated')

    fetchCompanies()

  } catch (error) {

    console.log(error)

    alert('Deactivate Failed')
  }
}
</script>

<style scoped>
.manage-companies-page {
  padding: 25px;
  background: #f1f5f9;
  min-height: 100vh;
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
.company-table-wrapper {
  background: white;

  border-radius: 18px;

  padding: 20px;

  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.company-table {
  margin-bottom: 0;
}

.company-table thead {
  background: #0f172a;
  color: white;
}

.company-table th,
.company-table td {
  vertical-align: middle;
  padding: 16px;
}

/* Company */
.company-info {
  display: flex;
  align-items: center;
  gap: 14px;
}

.company-logo {
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

.company-info h6 {
  margin-bottom: 2px;
  font-weight: 600;
}

.company-info small {
  color: #64748b;
}

/* Website */
.website-link {
  text-decoration: none;
  color: #2563eb;
  font-weight: 600;
}

/* Status */
.status-badge {
  padding: 6px 14px;

  border-radius: 30px;

  font-size: 13px;
  font-weight: 600;
}

.pending {
  background: #fef3c7;
  color: #92400e;
}

.approved {
  background: #dcfce7;
  color: #166534;
}

.deactivated {
  background: #fee2e2;
  color: #991b1b;
}

/* Buttons */
.action-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.approve-btn,
.reject-btn,
.delete-btn {
  border: none;

  padding: 8px 14px;

  border-radius: 10px;

  color: white;

  font-size: 14px;
  font-weight: 600;

  transition: 0.3s;
}

.approve-btn {
  background: #16a34a;
}

.reject-btn {
  background: #ea580c;
}

.delete-btn {
  background: #dc2626;
}

.approve-btn:hover,
.reject-btn:hover,
.delete-btn:hover {
  transform: translateY(-2px);
}

.deactivated-text {
  color: #dc2626;
  font-weight: 700;
  font-size: 14px;
}

/* Empty */
.empty-box {
  background: white;

  padding: 80px 20px;

  border-radius: 18px;

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

/* Responsive */
@media (max-width: 992px) {

  .company-table {
    min-width: 900px;
  }
}

@media (max-width: 576px) {

  .manage-companies-page {
    padding: 15px;
  }

  .search-box input {
    width: 100%;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>