<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { toast } from "vue3-toastify";
import { useRoute, useRouter } from "vue-router";
import FormContainer from "@/components/FormContainer.vue";

const route = useRoute();
const router = useRouter();
const id = route.params.id;

const sifra = ref("");
const naziv = ref("");
const godinaStudija = ref("");
const espb = ref("");
const status = ref("");
const errorMessage = ref("");

const fetchPredmet = async () => {
  try {
    const response = await axios.get(`/api/predmet/${id}`);
    sifra.value = response.data.sifra;
    naziv.value = response.data.naziv;
    godinaStudija.value = response.data.godina_studija;
    espb.value = response.data.espb;
    status.value = response.data.obavezni_izborni;
  } catch (error) {
    toast.error(error.response.data.message || error.message);
  }
};

const handleSubmit = async (event) => {
  event.preventDefault();
  try {
    const response = await axios.put(`/api/predmet-izmena/${id}`, {
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

onMounted(() => {
  fetchPredmet();
});
</script>

<template>
  <FormContainer title="Izmena predmeta">
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

      <div v-if="errorMessage" class="alert alert-danger mt-3">
        {{ errorMessage }}
      </div>
      <button type="submit" class="btn btn-primary mt-3">Sačuvaj</button>
    </form>
  </FormContainer>
</template>
