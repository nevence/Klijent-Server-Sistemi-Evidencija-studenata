<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter, RouterLink } from "vue-router";
import { toast } from "vue3-toastify";
import TableContainer from "@/components/TableContainer.vue";
import DeleteModal from "@/components/DeleteModal.vue";

const predmeti = ref([]);
const predmetToDelete = ref(null);
const router = useRouter();
const confirmModalRef = ref(null);

const fetchPredmeti = async () => {
  try {
    const response = await axios.get("/api/predmeti");
    predmeti.value = response.data;
  } catch (error) {
    toast.error(error.response.data.message || error.message);
  }
};

const confirmDelete = (predmet) => {
  predmetToDelete.value = predmet;
  confirmModalRef.value.showModal();
};

const deletePredmet = async () => {
  try {
    const response = await axios.delete(
      `/api/predmet-brisanje/${predmetToDelete.value.id}`
    );
    predmeti.value = predmeti.value.filter(
      (predmet) => predmet.id !== predmetToDelete.value.id
    );
    predmetToDelete.value = null;
    confirmModalRef.value.hideModal();
    toast.success(response.data.message);
  } catch (error) {
    toast.error(error.response.data.message || error.message);
  }
};

onMounted(() => {
  fetchPredmeti();
});
</script>

<template>
  <TableContainer to="/predmet-novi" buttonText="Dodaj predmet">
    <template #table-header>
      <tr>
        <th scope="col">Šifra</th>
        <th scope="col">Naziv</th>
        <th scope="col">Godina Studija</th>
        <th scope="col">ESPB</th>
        <th scope="col">Obavezni / Izborni</th>
        <th scope="col">Akcije</th>
      </tr>
    </template>
    <template #table-body>
      <tr v-for="predmet in predmeti" :key="predmet.id">
        <td>{{ predmet.sifra }}</td>
        <td>{{ predmet.naziv }}</td>
        <td>{{ predmet.godina_studija }}</td>
        <td>{{ predmet.espb }}</td>
        <td>{{ predmet.obavezni_izborni }}</td>
        <td>
          <button
            @click="router.push(`/predmet-izmena/${predmet.id}`)"
            role="button"
            class="text-warning mx-1 btn btn-link"
          >
            <i class="fas fa-edit"></i>
          </button>
          <button
            @click="confirmDelete(predmet)"
            class="text-danger mx-1 btn btn-link"
          >
            <i class="fas fa-trash"></i>
          </button>
        </td>
      </tr>
    </template>
  </TableContainer>

  <DeleteModal
    ref="confirmModalRef"
    :title="'Potvrda brisanja'"
    :message="'Da li ste sigurni da želite da obrišete predmet?'"
    :onConfirm="deletePredmet"
  />
</template>
