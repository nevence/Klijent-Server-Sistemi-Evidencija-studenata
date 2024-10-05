<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { toast } from "vue3-toastify";
import { useRouter, RouterLink } from "vue-router";
import TableContainer from "@/components/TableContainer.vue";
import DeleteModal from "@/components/DeleteModal.vue";

const korisnici = ref([]);
const korisnikToDelete = ref(null);
const confirmModalRef = ref(null);
const router = useRouter();

const fetchKorisnici = async () => {
  try {
    const response = await axios.get("/api/korisnici");
    korisnici.value = response.data;
  } catch (error) {
    toast.error(error.response.data.message || error.message);
  }
};

const confirmDelete = (korisnik) => {
  korisnikToDelete.value = korisnik;
  confirmModalRef.value.showModal();
};

const deleteKorisnik = async () => {
  try {
    const response = await axios.post(
      `/api/korisnik-brisanje/${korisnikToDelete.value.id}`
    );
    korisnici.value = korisnici.value.filter(
      (korisnik) => korisnik.id !== korisnikToDelete.value.id
    );
    korisnikToDelete.value = null;
    confirmModalRef.value.hideModal();
    toast.success(response.data.message);
  } catch (error) {
    toast.error(error.response.data.message || error.message);
  }
};

onMounted(() => {
  fetchKorisnici();
});
</script>

<template>
  <TableContainer to="/korisnik-novi" buttonText="Dodaj korisnika">
    <template #table-header>
      <tr>
        <th scope="col">Ime</th>
        <th scope="col">Prezime</th>
        <th scope="col">Email</th>
        <th scope="col">Rola</th>
        <th scope="col">Akcija</th>
      </tr>
    </template>
    <template #table-body>
      <tr v-for="korisnik in korisnici" :key="korisnik.id">
        <td>{{ korisnik.ime }}</td>
        <td>{{ korisnik.prezime }}</td>
        <td>{{ korisnik.email }}</td>
        <td>{{ korisnik.rola }}</td>
        <td>
          <button
            @click="router.push(`/korisnik-izmena/${korisnik.id}`)"
            role="button"
            class="text-warning mx-1 btn btn-link"
          >
            <i class="fas fa-edit"></i>
          </button>
          <button
            @click="confirmDelete(korisnik)"
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
    :message="'Da li ste sigurni da želite da obrišete korisnika?'"
    :onConfirm="deleteKorisnik"
  />
</template>
