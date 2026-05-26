<template>

  <div class="register-container">

    <div class="register-card">

      <h1 class="title">
        Company Registration
      </h1>

      <p class="subtitle">
        Register your company for campus placements
      </p>

      <form @submit.prevent="registerCompany">

        <!-- Company Name -->
        <div class="form-group">

          <label>Company Name</label>

          <input
            type="text"
            v-model="form.name"
            class="form-control"
            placeholder="Enter Company Name"
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
            placeholder="Enter Company Email"
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

        <!-- Website -->
        <div class="form-group">

          <label>Website</label>

          <input
            type="url"
            v-model="form.website"
            class="form-control"
            placeholder="Enter Company Website"
          />

        </div>

        <!-- HR Contact -->
        <div class="form-group">

          <label>HR Contact</label>

          <input
            type="text"
            v-model="form.hr_contact"
            class="form-control"
            placeholder="Enter HR Contact Number"
            required
          />

        </div>

        <!-- Submit -->
        <button
          type="submit"
          class="register-btn"
        >
          Register Company
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

  name: "CompanyRegisterView",

  data() {

    return {

      form: {

        name: "",
        email: "",
        password: "",

        role: "company",

        website: "",
        hr_contact: ""

      },

      message: ""

    };
  },

  methods: {

    async registerCompany() {

      try {

        const response = await axios.post(
          "http://127.0.0.1:5000/api/register",
          this.form
        );

        this.message = response.data.message;

        // Reset form
        this.form = {

          name: "",
          email: "",
          password: "",

          role: "company",

          website: "",
          hr_contact: ""

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

  box-sizing: border-box;
}

.form-control:focus {

  outline: none;

  border-color: #8e0dda9d;

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

</style>