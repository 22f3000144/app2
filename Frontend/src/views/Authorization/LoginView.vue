<template>
  <div class="login-container">

    <div class="login-card">

      <h1 class="title">
        Placement Portal Login
      </h1>

      <p class="subtitle">
        Login to continue
      </p>

      <form @submit.prevent="loginUser">

        <!-- Role Selection -->
        <div class="form-group">

          <label>Login As</label>

          <select
            v-model="selectedRole"
            class="form-control"
            required
          >
            <option value="">
              Select Role
            </option>

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

          <label>Email</label>

          <input
            type="email"
            v-model="form.email"
            class="form-control"
            placeholder="Enter Email"
            required
          />

        </div>

        <!-- Password -->
        <div class="form-group">

          <label>Password</label>

          <input
            type="password"
            v-model="form.password"
            class="form-control"
            placeholder="Enter Password"
            required
          />

        </div>

        <!-- Submit -->
        <button
          type="submit"
          class="login-btn"
        >
          Login
        </button>

      </form>

      <!-- Message -->
      <p
        v-if="message"
        class="message"
      >
        {{ message }}
      </p>


    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {

  name: "LoginView",

  data() {

    return {

      selectedRole: "",

      form: {

        email: "",
        password: ""

      },

      message: ""

    };
  },

  methods: {

    async loginUser() {

      try {

        const response = await axios.post(
          "http://127.0.0.1:5000/api/login",
          this.form
        );

        // Backend Role
        const backendRole = response.data.role;

        // Match dropdown role
        if (backendRole !== this.selectedRole) {

          this.message = "Selected role does not match account.";

          return;
        }

        // Store JWT
        localStorage.setItem(
          "token",
          response.data.access_token
        );

        localStorage.setItem(
          "role",
          response.data.role
        );

        localStorage.setItem(
          "name",
          response.data.name
        );

        this.message = response.data.message;

        // Redirect Based On Role
        if (backendRole === "admin") {

          this.$router.push("/admin-dashboard");

        }

        else if (backendRole === "student") {

          this.$router.push("/Studentdashboard/" + response.data.name);

        }

        else if (backendRole === "company") {

          this.$router.push("/company/dashboard");

        }

      }

      catch (error) {

        if (error.response) {

          this.message = error.response.data.message;

        }

        else {

          this.message = "Server Error";

        }
      }
    }
  }
};
</script>

<style scoped>

.login-container {

  min-height: 100vh;

  display: flex;

  justify-content: center;

  align-items: center;

  background-color: #f4f7fb;

  padding: 20px;
}

.login-card {

  width: 100%;

  max-width: 450px;

  background-color: white;

  padding: 40px;

  border-radius: 12px;

  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.title {

  text-align: center;

  font-size: 32px;

  font-weight: bold;

  margin-bottom: 10px;

  color: #1e3a8a;
}

.subtitle {

  text-align: center;

  color: #666;

  margin-bottom: 30px;
}

.form-group {

  margin-bottom: 20px;
}

label {

  display: block;

  margin-bottom: 8px;

  font-weight: 600;

  color: #333;
}

.form-control {

  width: 100%;

  padding: 12px;

  border: 1px solid #ccc;

  border-radius: 8px;

  font-size: 15px;

  transition: 0.3s;
}

.form-control:focus {

  outline: none;

  border-color: #2563eb;

  box-shadow: 0 0 5px rgba(37, 99, 235, 0.3);
}

.login-btn {

  width: 100%;

  padding: 14px;

  border: none;

  border-radius: 8px;

  background-color: #2563eb;

  color: white;

  font-size: 16px;

  font-weight: bold;

  cursor: pointer;

  transition: 0.3s;
}

.login-btn:hover {

  background-color: #1d4ed8;
}

.message {

  margin-top: 20px;

  text-align: center;

  font-weight: 600;

  color: green;
}

.register-links {

  margin-top: 25px;

  display: flex;

  justify-content: space-between;

  gap: 10px;
}

.register-links a {

  text-decoration: none;

  color: #2563eb;

  font-weight: 600;

  font-size: 14px;
}

.register-links a:hover {

  text-decoration: underline;
}

@media (max-width: 768px) {

  .login-card {

    padding: 25px;
  }

  .title {

    font-size: 26px;
  }

  .register-links {

    flex-direction: column;

    align-items: center;
  }
}

</style>