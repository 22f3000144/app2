<template>
  <div class="admin-profile-page">

    <!-- Header -->
    <div class="page-header">

      <div>
        <h2>Admin Profile</h2>
        <p>
          Manage your administrator account settings
        </p>
      </div>

    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading-box">
      Loading Profile...
    </div>

    <!-- Content -->
    <div v-else>

      <div class="profile-grid">

        <!-- Left -->
        <div class="profile-card">

          <div class="profile-top">

            <div class="profile-avatar">
              {{ profile.name?.charAt(0) }}
            </div>

            <h3>{{ profile.name }}</h3>

            <p>{{ profile.email }}</p>

            <span class="role-badge">
              Administrator
            </span>

          </div>

          <div class="profile-stats">

            <div class="stat-item">

              <h4>{{ profile.total_students || 0 }}</h4>

              <p>Students</p>

            </div>

            <div class="stat-item">

              <h4>{{ profile.total_companies || 0 }}</h4>

              <p>Companies</p>

            </div>

            <div class="stat-item">

              <h4>{{ profile.total_drives || 0 }}</h4>

              <p>Drives</p>

            </div>

          </div>

        </div>

        <!-- Right -->
        <div class="details-card">

          <div class="card-header">
            <h4>Profile Information</h4>
          </div>

          <form @submit.prevent="updateProfile">

            <div class="form-grid">

              <!-- Name -->
              <div class="form-group">

                <label>Full Name</label>

                <input
                  type="text"
                  v-model="form.name"
                  required
                />

              </div>

              <!-- Email -->
              <div class="form-group">

                <label>Email Address</label>

                <input
                  type="email"
                  v-model="form.email"
                  required
                />

              </div>

              <!-- Phone -->
              <div class="form-group">

                <label>Phone Number</label>

                <input
                  type="text"
                  v-model="form.phone"
                />

              </div>

              <!-- Department -->
              <div class="form-group">

                <label>Department</label>

                <input
                  type="text"
                  v-model="form.department"
                />

              </div>

            </div>

            <!-- Address -->
            <div class="form-group">

              <label>Office Address</label>

              <textarea
                rows="4"
                v-model="form.address"
              ></textarea>

            </div>

            <!-- Buttons -->
            <div class="button-group">

              <button
                type="submit"
                class="save-btn"
              >
                Update Profile
              </button>

              <button
                type="button"
                class="password-btn"
                @click="showPasswordModal = true"
              >
                Change Password
              </button>

            </div>

          </form>

        </div>

      </div>

    </div>

    <!-- Password Modal -->
    <div
      v-if="showPasswordModal"
      class="modal-overlay"
    >

      <div class="password-modal">

        <div class="modal-header">

          <h4>Change Password</h4>

          <button
            class="close-btn"
            @click="showPasswordModal = false"
          >
            ×
          </button>

        </div>

        <form @submit.prevent="changePassword">

          <div class="form-group">

            <label>Current Password</label>

            <input
              type="password"
              v-model="passwordForm.current_password"
              required
            />

          </div>

          <div class="form-group">

            <label>New Password</label>

            <input
              type="password"
              v-model="passwordForm.new_password"
              required
            />

          </div>

          <div class="form-group">

            <label>Confirm Password</label>

            <input
              type="password"
              v-model="passwordForm.confirm_password"
              required
            />

          </div>

          <button
            type="submit"
            class="save-btn full-btn"
          >
            Update Password
          </button>

        </form>

      </div>

    </div>

  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref } from 'vue'

const loading = ref(true)

const showPasswordModal = ref(false)

const profile = ref({})

const form = ref({
  name: '',
  email: '',
  phone: '',
  department: '',
  address: '',
})

const passwordForm = ref({
  current_password: '',
  new_password: '',
  confirm_password: '',
})

const fetchProfile = async () => {

  try {

    const token = localStorage.getItem('token')

    const response = await axios.get(
      'http://127.0.0.1:5000/api/profile',
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    profile.value = response.data || {}

    form.value.name = profile.value.name || ''
    form.value.email = profile.value.email || ''
    form.value.phone = profile.value.phone || ''
    form.value.department = profile.value.department || ''
    form.value.address = profile.value.address || ''

  } catch (error) {

    console.log(error)

  } finally {

    loading.value = false
  }
}

onMounted(() => {
  fetchProfile()
})

const updateProfile = async () => {

  try {

    const token = localStorage.getItem('token')

    await axios.put(
      'http://127.0.0.1:5000/api/admin/profile',
      form.value,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    alert('Profile Updated Successfully')

    fetchProfile()

  } catch (error) {

    console.log(error)

    alert('Update Failed')
  }
}

const changePassword = async () => {

  if (
    passwordForm.value.new_password !==
    passwordForm.value.confirm_password
  ) {

    alert('Passwords do not match')

    return
  }

  try {

    const token = localStorage.getItem('token')

    await axios.put(
      'http://127.0.0.1:5000/api/admin/change-password',
      passwordForm.value,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    alert('Password Updated Successfully')

    showPasswordModal.value = false

    passwordForm.value = {
      current_password: '',
      new_password: '',
      confirm_password: '',
    }

  } catch (error) {

    console.log(error)

    alert('Password Change Failed')
  }
}
</script>

<style scoped>
.admin-profile-page {
  min-height: 100vh;
  background: #f1f5f9;
  padding: 25px;
}

/* Header */
.page-header {
  margin-bottom: 30px;
}

.page-header h2 {
  font-weight: 700;
  margin-bottom: 5px;
}

.page-header p {
  color: #64748b;
}

/* Grid */
.profile-grid {
  display: grid;
  grid-template-columns: 320px 1fr;

  gap: 25px;
}

/* Profile Card */
.profile-card {
  background: white;

  border-radius: 20px;

  padding: 30px 25px;

  box-shadow: 0 4px 15px rgba(0,0,0,0.05);

  height: fit-content;
}

.profile-top {
  text-align: center;
}

.profile-avatar {
  width: 110px;
  height: 110px;

  border-radius: 50%;

  background: #2563eb;
  color: white;

  margin: auto;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 40px;
  font-weight: 700;

  margin-bottom: 18px;
}

.profile-top h3 {
  margin-bottom: 6px;
  font-weight: 700;
}

.profile-top p {
  color: #64748b;
}

.role-badge {
  display: inline-block;

  margin-top: 12px;

  background: #dbeafe;
  color: #1d4ed8;

  padding: 8px 16px;

  border-radius: 30px;

  font-size: 14px;
  font-weight: 600;
}

/* Stats */
.profile-stats {
  margin-top: 30px;

  display: flex;
  justify-content: space-between;

  gap: 15px;
}

.stat-item {
  flex: 1;

  background: #f8fafc;

  border-radius: 14px;

  padding: 18px;

  text-align: center;
}

.stat-item h4 {
  font-weight: 700;
  margin-bottom: 6px;
}

.stat-item p {
  color: #64748b;
  font-size: 14px;
}

/* Details */
.details-card {
  background: white;

  border-radius: 20px;

  padding: 30px;

  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.card-header {
  margin-bottom: 25px;
}

.card-header h4 {
  font-weight: 700;
}

/* Form */
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));

  gap: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;

  margin-bottom: 8px;

  font-weight: 600;
}

.form-group input,
.form-group textarea {
  width: 100%;

  border: 1px solid #dbe2ea;
  outline: none;

  padding: 12px 15px;

  border-radius: 12px;

  background: #f8fafc;
}

.form-group textarea {
  resize: none;
}

/* Buttons */
.button-group {
  display: flex;
  gap: 15px;

  flex-wrap: wrap;

  margin-top: 10px;
}

.save-btn,
.password-btn {
  border: none;

  padding: 12px 20px;

  border-radius: 12px;

  color: white;

  font-weight: 600;

  transition: 0.3s;
}

.save-btn {
  background: #2563eb;
}

.password-btn {
  background: #0f172a;
}

.save-btn:hover,
.password-btn:hover {
  transform: translateY(-2px);
}

.full-btn {
  width: 100%;
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

.password-modal {
  width: 100%;
  max-width: 500px;

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

/* Responsive */
@media (max-width: 992px) {

  .profile-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 576px) {

  .admin-profile-page {
    padding: 15px;
  }

  .details-card,
  .profile-card {
    padding: 20px;
  }

  .button-group {
    flex-direction: column;
  }

  .save-btn,
  .password-btn {
    width: 100%;
  }

  .password-modal {
    margin: 15px;
  }
}
</style>