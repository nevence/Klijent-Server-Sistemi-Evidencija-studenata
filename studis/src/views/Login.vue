<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { toast } from "vue3-toastify";

const email = ref("");
const lozinka = ref("");
const router = useRouter();

const handleSubmit = async (event) => {
  event.preventDefault();
  try {
    const response = await axios.post("/api/login", {
      email: email.value,
      lozinka: lozinka.value,
    });

    localStorage.setItem("access_token", response.data.access_token);
    localStorage.setItem("rola", response.data.rola);

    router.push("/studenti").then(() => toast.success(response.data.message));
  } catch (error) {
    toast.error(error.response.data.message || error.message);
  }
};
</script>

<template>
  <div class="container">
    <div class="row justify-content-center my-5">
      <img src="@/assets/img/logo.png" class="img-fluid logo" alt="Logo" />
    </div>
    <div class="row justify-content-center">
      <div class="col-lg-6 col-xs-12">
        <form @submit="handleSubmit">
          <div class="form-group mb-3">
            <label>Email adresa</label>
            <input type="email" v-model="email" class="form-control" required />
          </div>
          <div class="form-group mb-3">
            <label>Lozinka</label>
            <input
              type="password"
              v-model="lozinka"
              class="form-control"
              required
            />
          </div>
          <input
            type="submit"
            class="btn btn-primary"
            role="button"
            value="Prijavi se"
          />
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.logo {
  width: 20rem;
  height: auto;
}
</style>
