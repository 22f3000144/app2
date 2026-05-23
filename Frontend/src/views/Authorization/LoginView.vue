<template>
  <div class="login-page">

    <!-- ======================================
    LEFT SECTION
    ======================================= -->

    <div class="login-left">

      <div class="overlay">

        <div class="brand-content">

          <h1>Eduvora</h1>

          <p>
            Smart Placement Management Portal
          </p>

          <div class="features">

            <div class="feature-item">

              <i class="bi bi-check-circle-fill"></i>

              Student Placement Tracking

            </div>

            <div class="feature-item">

              <i class="bi bi-check-circle-fill"></i>

              Company Recruitment Management

            </div>

            <div class="feature-item">

              <i class="bi bi-check-circle-fill"></i>

              Real-time Analytics & Reports

            </div>

          </div>

        </div>

      </div>

    </div>


    <!-- ======================================
    RIGHT SECTION
    ======================================= -->

    <div class="login-right">

      <div class="login-card">

        <!-- Header -->
        <div class="login-header">

          <h2>Welcome Back</h2>

          <p>
            Login to continue
          </p>

        </div>

        <!-- Error Message -->
        <div
          v-if="message"
          class="message-box"
        >
          {{ message }}
        </div>

        <!-- Login Form -->
        <form @submit.prevent="loginUser">

          <!-- Role -->
          <div class="form-group">

            <label>Select Role</label>

            <select v-model="selectedRole">

              <option value="student">
                Student
              </option>

              <option value="company">
                Company
              </option>

              <option value="admin">
                Admin
              </option>

            </select>

          </div>

          <!-- Email -->
          <div class="form-group">

            <label>Email Address</label>

            <input
              type="email"
              placeholder="Enter email"
              v-model="form.email"
              required
            />

          </div>

          <!-- Password -->
          <div class="form-group">

            <label>Password</label>

            <input
              type="password"
              placeholder="Enter password"
              v-model="form.password"
              required
            />

          </div>

          <!-- Login Button -->
          <button
            type="submit"
            class="login-btn"
            :disabled="loading"
          >

            <span v-if="loading">
              Logging In...
            </span>

            <span v-else>
              Login
            </span>

          </button>

        </form>

        <!-- Footer -->
        <div class="login-footer">

          <p>
            Don't have an account?
          </p>

          <RouterLink to="/register">
            Register Here
          </RouterLink>

        </div>

      </div>

    </div>

  </div>
</template>

<script setup>

import axios from 'axios'

import { ref } from 'vue'

import {
  RouterLink,
  useRouter,
} from 'vue-router'


// ======================================
// ROUTER
// ======================================

const router = useRouter()


// ======================================
// REACTIVE VARIABLES
// ======================================

const loading = ref(false)

const message = ref('')

const selectedRole = ref('student')

const form = ref({

  email: '',
  password: '',

})


// ======================================
// LOGIN FUNCTION
// ======================================

const loginUser = async () => {

  loading.value = true

  message.value = ''

  try {

    // ======================================
    // API CALL
    // ======================================

    const response = await axios.post(

      'http://127.0.0.1:5000/api/login',

      form.value

    )

    const data = response.data


    // ======================================
    // ROLE VALIDATION
    // ======================================

    if (

      data.user?.role?.toLowerCase() !==
      selectedRole.value.toLowerCase()

    ) {

      message.value =
        'Selected role does not match account.'

      loading.value = false

      return

    }


    // ======================================
    // SAVE TOKEN
    // ======================================

    localStorage.setItem(
      'token',
      data.access_token
    )


    // ======================================
    // SAVE USER
    // ======================================

    localStorage.setItem(

      'user',

      JSON.stringify(data.user)

    )


    // ======================================
    // REDIRECT USER
    // ======================================

    if (

      data.user.role.toLowerCase() === 'admin'

    ) {

      router.push('/admin')

    }

    else if (

      data.user.role.toLowerCase() === 'company'

    ) {

      router.push(`/company-dashboard/${data.user.name}`)

    }

    else if (

      data.user.role.toLowerCase() === 'student'

    ) {

      router.push(`/student-dashboard/${data.user.name}`)

    }

    else {

      router.push('/')

    }

  }

  catch (error) {

    console.log(error)

    if (

      error.response?.data?.message

    ) {

      message.value =
        error.response.data.message

    }

    else {

      message.value =
        'Login failed. Please try again.'

    }

  }

  finally {

    loading.value = false

  }

}

</script>

<style scoped>

/* ======================================
MAIN LAYOUT
====================================== */

.login-page {

  display: grid;
  grid-template-columns: 1fr 1fr;

  min-height: 100vh;

}


/* ======================================
LEFT SECTION
====================================== */

.login-left {

  background:
    linear-gradient(
      rgba(15,23,42,0.82),
      rgba(37,99,235,0.82)
    ),
    url('https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=1200');

  background-size: cover;
  background-position: center;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 40px;

}

.overlay {

  color: white;

}

.brand-content h1 {

  font-size: 58px;
  font-weight: 800;

  margin-bottom: 18px;

}

.brand-content p {

  font-size: 20px;

  color: #e2e8f0;

  margin-bottom: 40px;

}

.features {

  display: flex;
  flex-direction: column;

  gap: 20px;

}

.feature-item {

  display: flex;
  align-items: center;

  gap: 14px;

  font-size: 17px;

}

.feature-item i {

  color: #22c55e;

}


/* ======================================
RIGHT SECTION
====================================== */

.login-right {

  display: flex;
  align-items: center;
  justify-content: center;

  background: #f8fafc;

  padding: 30px;

}


/* ======================================
LOGIN CARD
====================================== */

.login-card {

  width: 100%;
  max-width: 450px;

  background: white;

  padding: 40px;

  border-radius: 24px;

  box-shadow: 0 8px 25px rgba(0,0,0,0.08);

}

.login-header {

  margin-bottom: 30px;

}

.login-header h2 {

  font-size: 34px;
  font-weight: 700;

  margin-bottom: 8px;

}

.login-header p {

  color: #64748b;

}


/* ======================================
FORM
====================================== */

.form-group {

  margin-bottom: 20px;

}

.form-group label {

  display: block;

  margin-bottom: 8px;

  font-weight: 600;

}

.form-group input,
.form-group select {

  width: 100%;

  border: 1px solid #dbe2ea;

  outline: none;

  padding: 14px 16px;

  border-radius: 14px;

  background: #f8fafc;

  font-size: 15px;

}


/* ======================================
BUTTON
====================================== */

.login-btn {

  width: 100%;

  border: none;

  background: #2563eb;
  color: white;

  padding: 14px;

  border-radius: 14px;

  font-size: 16px;
  font-weight: 600;

  margin-top: 10px;

  transition: 0.3s;

  cursor: pointer;

}

.login-btn:hover {

  background: #1d4ed8;

}

.login-btn:disabled {

  opacity: 0.7;

  cursor: not-allowed;

}


/* ======================================
FOOTER
====================================== */

.login-footer {

  text-align: center;

  margin-top: 25px;

}

.login-footer p {

  color: #64748b;

  margin-bottom: 8px;

}

.login-footer a {

  text-decoration: none;

  color: #2563eb;

  font-weight: 600;

}


/* ======================================
MESSAGE BOX
====================================== */

.message-box {

  background: #fee2e2;

  color: #991b1b;

  padding: 14px;

  border-radius: 12px;

  margin-bottom: 20px;

}


/* ======================================
RESPONSIVE
====================================== */

@media (max-width: 992px) {

  .login-page {

    grid-template-columns: 1fr;

  }

  .login-left {

    display: none;

  }

}

@media (max-width: 576px) {

  .login-right {

    padding: 18px;

  }

  .login-card {

    padding: 25px;

  }

  .brand-content h1 {

    font-size: 42px;

  }

}

</style>