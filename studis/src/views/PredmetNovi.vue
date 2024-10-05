<script setup>
import { ref } from "vue";
import axios from "axios";
import FormContainer from "@/components/FormContainer.vue";
import { useRouter } from "vue-router";
import { toast } from "vue3-toastify";

const router = useRouter();

const sifra = ref("");
const naziv = ref("");
const godinaStudija = ref("");
const espb = ref("");
const status = ref("");

const handleSubmit = async (event) => {
  event.preventDefault();
  try {
    const response = await axios.post("/api/predmet-novi", {
      sifra: sifra.value,
      naziv: naziv.value,
      godina_studija: godinaStudija.value,
      espb: espb.value,
      status: status.value,
    });
    router.push("/predmeti").then(() => toast.success(response.data.message));
  } catch (error) {
    toast.error(error.response.data.message || error.message);
  }
};
</script>

<template>
  <FormContainer title="Novi predmet">
    <form @submit="handleSubmit">
      <div class="mb-3">
        <label for="sifra" class="form-label">Šifra</label>
        <input
          type="text"
          class="form-control"
          id="sifra"
          v-model="sifra"
          required
        />
      </div>

      <div class="mb-3">
        <label for="naziv" class="form-label">Naziv</label>
        <input
          type="text"
          class="form-control"
          id="naziv"
          v-model="naziv"
          required
        />
      </div>

      <div class="mb-3">
        <label for="godinaStudija" class="form-label">Godina studija</label>
        <input
          type="text"
          class="form-control"
          id="godinaStudija"
          v-model="godinaStudija"
          required
        />
      </div>

      <div class="mb-3">
        <label for="espb" class="form-label">ESPB</label>
        <input
          type="text"
          class="form-control"
          id="espb"
          v-model="espb"
          required
        />
      </div>

      <div class="mb-3">
        <label for="status" class="form-label">Obavezni / Izborni</label>
        <select id="status" class="form-select" v-model="status" required>
          <option selected disabled value=""></option>
          <option value="obavezni">Obavezni</option>
          <option value="izborni">Izborni</option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary mt-3">Sačuvaj</button>
    </form>
  </FormContainer>
</template>
