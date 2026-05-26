<template>
  <div class="company-profile-page">

    <!-- Header -->
    <div class="page-header">

      <div>

        <h2>Company Profile</h2>

        <p>
          Manage your company information and profile details
        </p>

      </div>

      <button
        class="edit-btn"
        @click="enableEdit"
        v-if="!editMode"
      >
        Edit Profile
      </button>

    </div>

    <!-- Loading -->
    <div
      v-if="loading"
      class="loading-box"
    >
      Loading profile...
    </div>

    <!-- Profile -->
    <div
      v-else
      class="profile-wrapper"
    >

      <!-- Left -->
      <div class="profile-sidebar">

        <div class="profile-card">

          <div class="company-avatar">

            {{
              profile.company_name
                ?.charAt(0)
                ?.toUpperCase()
            }}

          </div>

          <h3>
            {{ profile.company_name }}
          </h3>

          <p>
            {{ profile.industry }}
          </p>

          <span
            class="status-badge"
            :class="profile.approved
              ? 'approved'
              : 'pending'"
          >

            {{
              profile.approved
                ? "Approved"
                : "Pending Approval"
            }}

          </span>

        </div>

      </div>

      <!-- Right -->
      <div class="profile-content">

        <div class="profile-card">

          <div class="card-header">

            <h3>
              Company Information
            </h3>

          </div>

          <form @submit.prevent="updateProfile">

            <div class="form-grid">

              <!-- Company Name -->
              <div class="form-group">

                <label>
                  Company Name
                </label>

                <input
                  type="text"
                  v-model="form.company_name"
                  :disabled="!editMode"
                />

              </div>

              <!-- Industry -->
              <div class="form-group">

                <label>
                  Industry
                </label>

                <input
                  type="text"
                  v-model="form.industry"
                  :disabled="!editMode"
                />

              </div>

              <!-- Email -->
              <div class="form-group">

                <label>
                  Email
                </label>

                <input
                  type="email"
                  v-model="form.email"
                  disabled
                />

              </div>

              <!-- HR Contact -->
              <div class="form-group">

                <label>
                  HR Contact
                </label>

                <input
                  type="text"
                  v-model="form.hr_contact"
                  :disabled="!editMode"
                />

              </div>

              <!-- Website -->
              <div class="form-group">

                <label>
                  Website
                </label>

                <input
                  type="url"
                  v-model="form.website"
                  :disabled="!editMode"
                />

              </div>

              <!-- Location -->
              <div class="form-group">

                <label>
                  Location
                </label>

                <input
                  type="text"
                  v-model="form.location"
                  :disabled="!editMode"
                />

              </div>

            </div>

            <!-- Description -->
            <div class="form-group">

              <label>
                Company Description
              </label>

              <textarea
                rows="6"
                v-model="form.company_description"
                :disabled="!editMode"
              ></textarea>

            </div>

            <!-- Buttons -->
            <div
              v-if="editMode"
              class="button-group"
            >

              <button
                type="submit"
                class="save-btn"
                :disabled="updating"
              >

                <span v-if="updating">
                  Saving...
                </span>

                <span v-else>
                  Save Changes
                </span>

              </button>

              <button
                type="button"
                class="cancel-btn"
                @click="cancelEdit"
              >
                Cancel
              </button>

            </div>

          </form>

        </div>

        <!-- Account Info -->
        <div class="profile-card">

          <div class="card-header">

            <h3>
              Account Information
            </h3>

          </div>

          <div class="account-grid">

            <div class="account-item">

              <label>
                Account Status
              </label>

              <span>
                {{
                  profile.active
                    ? "Active"
                    : "Deactivated"
                }}
              </span>

            </div>

            <div class="account-item">

              <label>
                Role
              </label>

              <span>
                {{ profile.role }}
              </span>

            </div>

            <div class="account-item">

              <label>
                Company ID
              </label>

              <span>
                #{{ profile.id }}
              </span>

            </div>

          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {

  name: "CompanyProfileView",

  data() {

    return {

      loading: true,

      updating: false,

      editMode: false,

      profile: {},

      form: {

        company_name: "",
        industry: "",
        email: "",
        hr_contact: "",
        website: "",
        location: "",
        company_description: ""

      }

    };

  },

  mounted() {

    this.fetchProfile();

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

    async fetchProfile() {

      try {

        const response = await axios.get(

          "http://127.0.0.1:5000/api/company/dashboard",

          this.getHeaders()

        );

        this.profile =
          response.data.company;

        this.form = {

          company_name:
            this.profile.company_name,

          industry:
            this.profile.industry,

          email:
            this.profile.email,

          hr_contact:
            this.profile.hr_contact,

          website:
            this.profile.website,

          location:
            this.profile.location,

          company_description:
            this.profile.company_description

        };

      }

      catch (error) {

        console.error(error);

        alert(

          error.response?.data?.message ||

          "Failed to load profile."

        );

      }

      finally {

        this.loading = false;

      }

    },

    enableEdit() {

      this.editMode = true;

    },

    cancelEdit() {

      this.editMode = false;

      this.form = {

        company_name:
          this.profile.company_name,

        industry:
          this.profile.industry,

        email:
          this.profile.email,

        hr_contact:
          this.profile.hr_contact,

        website:
          this.profile.website,

        location:
          this.profile.location,

        company_description:
          this.profile.company_description

      };

    },

    async updateProfile() {

      try {

        this.updating = true;

        /*
          Replace endpoint
          with your update API
        */

        await axios.put(

          "http://127.0.0.1:5000/api/profile",

          this.form,

          this.getHeaders()

        );

        alert(
          "Profile updated successfully."
        );

        this.editMode = false;

        this.fetchProfile();

      }

      catch (error) {

        console.error(error);

        alert(

          error.response?.data?.message ||

          "Failed to update profile."

        );

      }

      finally {

        this.updating = false;

      }

    }

  }

};
</script>

<style scoped>

.company-profile-page {

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

.edit-btn {

  border: none;

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

  cursor: pointer;

  transition: 0.3s;

}

.edit-btn:hover {

  transform: translateY(-2px);

}

/* =========================
   LOADING
========================= */

.loading-box {

  background: white;

  padding: 50px;

  border-radius: 24px;

  text-align: center;
  font-weight: 700;

}

/* =========================
   LAYOUT
========================= */

.profile-wrapper {

  display: grid;

  grid-template-columns:
    320px 1fr;

  gap: 24px;

}

.profile-card {

  background: white;

  border-radius: 26px;

  padding: 28px;

  box-shadow:
    0 15px 40px rgba(0,0,0,0.05);

}

/* =========================
   SIDEBAR
========================= */

.profile-sidebar {

  position: sticky;
  top: 20px;

  height: fit-content;

}

.company-avatar {

  width: 110px;
  height: 110px;

  margin: auto;

  border-radius: 50%;

  background:
    linear-gradient(
      135deg,
      #7c3aed,
      #dc2626
    );

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 42px;
  font-weight: bold;

  color: white;

  margin-bottom: 24px;

}

.profile-sidebar h3 {

  text-align: center;

  margin-bottom: 8px;

  color: #1e1b4b;

}

.profile-sidebar p {

  text-align: center;

  color: #64748b;

  margin-bottom: 20px;

}

.status-badge {

  display: block;

  width: fit-content;

  margin: auto;

  padding: 8px 16px;

  border-radius: 50px;

  font-size: 13px;
  font-weight: 700;

}

.status-badge.approved {

  background: #dcfce7;
  color: #16a34a;

}

.status-badge.pending {

  background: #fef3c7;
  color: #d97706;

}

/* =========================
   CONTENT
========================= */

.card-header {

  margin-bottom: 24px;

}

.card-header h3 {

  margin: 0;
  color: #1e1b4b;

}

.form-grid {

  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(240px, 1fr));

  gap: 20px;

}

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

  transition: 0.3s;

}

.form-group input:focus,
.form-group textarea:focus {

  border-color: #7c3aed;

  box-shadow:
    0 0 0 4px rgba(124,58,237,0.08);

  background: white;

}

.form-group input:disabled,
.form-group textarea:disabled {

  background: #f8fafc;
  cursor: not-allowed;

}

/* =========================
   BUTTONS
========================= */

.button-group {

  display: flex;
  gap: 14px;
  flex-wrap: wrap;

  margin-top: 10px;

}

.save-btn,
.cancel-btn {

  border: none;

  padding: 14px 22px;

  border-radius: 14px;

  font-weight: 700;

  cursor: pointer;

}

.save-btn {

  background:
    linear-gradient(
      135deg,
      #7c3aed,
      #dc2626
    );

  color: white;

}

.cancel-btn {

  background: #f1f5f9;
  color: #334155;

}

/* =========================
   ACCOUNT
========================= */

.account-grid {

  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(200px, 1fr));

  gap: 20px;

}

.account-item {

  background: #fafafa;

  border-radius: 18px;

  padding: 20px;

}

.account-item label {

  display: block;

  font-size: 13px;

  color: #64748b;

  margin-bottom: 10px;

}

.account-item span {

  font-size: 18px;
  font-weight: 700;

  color: #1e293b;

}

/* =========================
   RESPONSIVE
========================= */

@media (max-width: 992px) {

  .profile-wrapper {

    grid-template-columns: 1fr;

  }

  .profile-sidebar {

    position: relative;

  }

}

@media (max-width: 768px) {

  .company-profile-page {

    padding: 18px;

  }

  .page-header {

    flex-direction: column;
    align-items: flex-start;

  }

  .page-header h2 {

    font-size: 28px;

  }

  .button-group {

    flex-direction: column;

  }

  .save-btn,
  .cancel-btn {

    width: 100%;

  }

}

</style>