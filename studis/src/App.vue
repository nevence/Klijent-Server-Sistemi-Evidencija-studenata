<script setup>
import { RouterLink, RouterView } from "vue-router";
import Navbar from "./components/Navbar.vue";
</script>

<template>
  <div>
    <Navbar v-if="$route.name !== 'Login'"></Navbar>
    <RouterView></RouterView>
  </div>
</template>

<style>
/* Stilovi za aplikaciju */
</style>
