<script setup>
import { RouterLink, useRoute } from "vue-router";
import { useRouter } from "vue-router";
import { useUserRole } from "@/composables/useUserRole.js";
import { toast } from "vue3-toastify";
import { onMounted } from "vue";

const router = useRouter();
const { userRole, checkUserRole } = useUserRole();

const isActiveLink = (routePath) => {
  const route = useRoute();
  return route.path === routePath;
};

onMounted(() => {
  checkUserRole();
});

const handleLogout = async () => {
  try {
    localStorage.removeItem("access_token");
    localStorage.removeItem("rola");
    router.push("/login").then(() => toast.success("Uspešno ste se odjavili."));
  } catch (error) {
    toast.error(error.response.data.message || error.message);
  }
};
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
      <RouterLink class="navbar-brand" to="/studenti"
        >Studentska evidencija</RouterLink
      >
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li :class="{ 'nav-item': true, active: isActiveLink('/studenti') }">
            <RouterLink class="nav-link" to="/studenti">Studenti</RouterLink>
          </li>
          <li
            v-if="userRole === 'administrator'"
            :class="{ 'nav-item': true, active: isActiveLink('/predmeti') }"
          >
            <RouterLink class="nav-link" to="/predmeti">Predmeti</RouterLink>
          </li>
          <li
            v-if="userRole === 'administrator'"
            :class="{ 'nav-item': true, active: isActiveLink('/korisnici') }"
          >
            <RouterLink class="nav-link" to="/korisnici">Korisnici</RouterLink>
          </li>
        </ul>
        <form class="d-flex" @submit.prevent="handleLogout">
          <button type="submit" class="btn btn-primary">
            <i class="fas fa-sign-out-alt"></i>
          </button>
        </form>
      </div>
    </div>
  </nav>
</template>
