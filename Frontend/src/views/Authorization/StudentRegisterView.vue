<template>
  <div class="register-container">

    <div class="register-card">

      <h1 class="title">
        Student Registration
      </h1>

      <p class="subtitle">
        Register for campus placement opportunities
      </p>

      <form @submit.prevent="registerStudent">

        <!-- Full Name -->
        <div class="form-group">

          <label>Full Name</label>

          <input
            type="text"
            v-model="form.name"
            class="form-control"
            placeholder="Enter Full Name"
            required
          />

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

        <!-- Branch -->
        <div class="form-group">

          <label>Branch</label>

          <input
            type="text"
            v-model="form.branch"
            class="form-control"
            placeholder="Enter Branch"
            required
          />

        </div>

        <!-- CGPA -->
        <div class="form-group">

          <label>CGPA</label>

          <input
            type="number"
            step="0.01"
            v-model="form.cgpa"
            class="form-control"
            placeholder="Enter CGPA"
            required
          />

        </div>

        <!-- Passing Year -->
        <div class="form-group">

          <label>Passing Year</label>

          <input
            type="number"
            v-model="form.year"
            class="form-control"
            placeholder="Enter Passing Year"
            required
          />

        </div>

        <!-- Resume -->
        <div class="form-group">

          <label>Resume Link (Optional)</label>

          <input
            type="text"
            v-model="form.resume"
            class="form-control"
            placeholder="Resume URL or File Name"
          />

        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          class="register-btn"
        >
          Register Student
        </button>

      </form>

      <!-- Response Message -->
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

  name: "StudentRegisterView",

  data() {

    return {

      form: {

        name: "",
        email: "",
        password: "",

        role: "student",

        branch: "",
        cgpa: "",
        year: "",
        resume: ""

      },

      message: ""

    };
  },

  methods: {

    async registerStudent() {

      try {

        const response = await axios.post(
          "http://127.0.0.1:5000/api/register",
          this.form
        );

        this.message = response.data.message;

        // Reset Form
        this.form = {

          name: "",
          email: "",
          password: "",

          role: "student",

          branch: "",
          cgpa: "",
          year: "",
          resume: ""

        };

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

.register-container {

  min-height: 100vh;

  display: flex;

  justify-content: center;

  align-items: center;

  background-color: #f4f7fb;

  padding: 20px;
}

.register-card {

  width: 100%;

  max-width: 500px;

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

.register-btn {

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

.register-btn:hover {

  background-color: #1d4ed8;
}

.message {

  margin-top: 20px;

  text-align: center;

  font-weight: 600;

  color: green;
}

@media (max-width: 768px) {

  .register-card {

    padding: 25px;
  }

  .title {

    font-size: 26px;
  }
}
.register-links {

  margin-top: 25px;

  display: flex;

  justify-content: space-between;

  gap: 10px;
}

.register-links a {

  text-decoration: none;

  color: #9225eb;

  font-weight: 600;

  font-size: 14px;
}

.register-links a:hover {

  text-decoration: underline;
}


</style>