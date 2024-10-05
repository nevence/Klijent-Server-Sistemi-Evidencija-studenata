<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { toast } from "vue3-toastify";
import FormContainer from "@/components/FormContainer.vue";

const router = useRouter();
const errorMessage = ref("");

const brojIndeksa = ref("");
const ime = ref("");
const prezime = ref("");
const imeRoditelja = ref("");
const email = ref("");
const telefon = ref("");
const godinaStudija = ref("");
const datumRodjenja = ref("");
const jmbg = ref("");

const handleSubmit = async (event) => {
  event.preventDefault();
  try {
    const response = await axios.post("/api/student-novi", {
      broj_indeksa: brojIndeksa.value,
      ime: ime.value,
      prezime: prezime.value,
      ime_roditelja: imeRoditelja.value,
      email: email.value,
      broj_telefona: telefon.value,
      godina_studija: godinaStudija.value,
      datum_rodjenja: datumRodjenja.value,
      jmbg: jmbg.value,
    });
    router.push("/studenti").then(() => toast.success(response.data.message));
  } catch (error) {
    toast.error(error.response.data.message || error.message);
  }
};
</script>

<template>
  <FormContainer title="Novi student">
    <form @submit="handleSubmit">
      <div class="row">
        <div class="col-md-6 mb-3">
          <label for="br_indeks" class="form-label">Broj indeksa</label>
          <input
            type="text"
            class="form-control"
            id="br_indeks"
            v-model="brojIndeksa"
            required
          />
        </div>

        <div class="col-md-6 mb-3">
          <label for="ime" class="form-label">Ime</label>
          <input
            type="text"
            class="form-control"
            id="ime"
            v-model="ime"
            required
          />
        </div>

        <div class="col-md-6 mb-3">
          <label for="prezime" class="form-label">Prezime</label>
          <input
            type="text"
            class="form-control"
            id="prezime"
            v-model="prezime"
            required
          />
        </div>

        <div class="col-md-6 mb-3">
          <label for="ime_roditelja" class="form-label">Ime roditelja</label>
          <input
            type="text"
            class="form-control"
            id="ime_roditelja"
            v-model="imeRoditelja"
            required
          />
        </div>

        <div class="col-md-6 mb-3">
          <label for="email" class="form-label">Email</label>
          <input
            type="email"
            class="form-control"
            id="email"
            v-model="email"
            required
          />
        </div>

        <div class="col-md-6 mb-3">
          <label for="telefon" class="form-label">Broj telefona</label>
          <input
            type="text"
            class="form-control"
            id="telefon"
            v-model="telefon"
            required
          />
        </div>

        <div class="col-md-6 mb-3">
          <label for="god_studija" class="form-label">Godina studija</label>
          <select
            id="god_studija"
            class="form-select"
            v-model="godinaStudija"
            required
          >
            <option selected disabled value="">Izaberi godinu</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
          </select>
        </div>

        <div class="col-md-6 mb-3">
          <label for="datum" class="form-label">Datum rođenja</label>
          <input
            type="date"
            class="form-control"
            id="datum"
            v-model="datumRodjenja"
            required
          />
        </div>

        <div class="col-md-6 mb-3">
          <label for="jmbg" class="form-label">JMBG</label>
          <input
            type="text"
            class="form-control"
            id="jmbg"
            v-model="jmbg"
            required
          />
        </div>
      </div>

      <button type="submit" class="btn btn-primary">Sačuvaj</button>
    </form>
  </FormContainer>
</template>
