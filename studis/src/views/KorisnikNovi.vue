<script setup>
import { ref } from "vue";
import axios from "axios";
import { toast } from "vue3-toastify";
import { useRouter } from "vue-router";
import FormContainer from "@/components/FormContainer.vue";

const router = useRouter();

const ime = ref("");
const prezime = ref("");
const email = ref("");
const rola = ref("");
const lozinka = ref("");

const handleSubmit = async (event) => {
  event.preventDefault();
  try {
    const response = await axios.post("/api/korisnik-novi", {
      ime: ime.value,
      prezime: prezime.value,
      email: email.value,
      rola: rola.value,
      lozinka: lozinka.value,
    });
    router.push("/korisnici").then(() => toast.success(response.data.message));
  } catch (error) {
    toast.error(error.response.data.message || error.message);
  }
};
</script>

<template>
  <FormContainer title="Novi korisnik">
    <form @submit="handleSubmit">
      <div class="mb-3">
        <label for="ime" class="form-label">Ime</label>
        <input
          type="text"
          class="form-control"
          id="ime"
          v-model="ime"
          required
        />
      </div>

      <div class="mb-3">
        <label for="prezime" class="form-label">Prezime</label>
        <input
          type="text"
          class="form-control"
          id="prezime"
          v-model="prezime"
          required
        />
      </div>

      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input
          type="email"
          class="form-control"
          id="email"
          v-model="email"
          required
        />
      </div>

      <div class="mb-3">
        <label for="rola" class="form-label">Rola</label>
        <select id="rola" class="form-select" v-model="rola" required>
          <option selected disabled value="">Izaberi rolu</option>
          <option value="administrator">Administrator</option>
          <option value="profesor">Profesor</option>
        </select>
      </div>

      <div class="mb-3">
        <label for="lozinka" class="form-label">Lozinka</label>
        <input
          type="password"
          class="form-control"
          id="lozinka"
          v-model="lozinka"
          required
        />
      </div>

      <button type="submit" class="btn btn-primary">Sačuvaj</button>
    </form>
  </FormContainer>
</template>
