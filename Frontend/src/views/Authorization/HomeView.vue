<script setup>
import { RouterLink, RouterView, useRoute } from 'vue-router'
// import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
        <!-- Public Header -->
  <header>
    <img
      alt="App logo"
      class="logo"
      src="@/assets/logo.png"
      width="125"
      height="125"
    />

    <div class="wrapper">
      <HelloWorld msg="Eduvora" />

      <nav>
        <RouterLink to="/">Home</RouterLink>

        <RouterLink to="/login">
          Login
        </RouterLink>

        <RouterLink to="/company-register">
          Company Sign Up
        </RouterLink>

        <RouterLink to="/student-register">
          Student Sign Up
        </RouterLink>
      </nav>
    </div>
  </header>
</template>
