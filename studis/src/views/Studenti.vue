<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { toast } from "vue3-toastify";
import { useRouter, RouterLink } from "vue-router";
import TableContainer from "@/components/TableContainer.vue";
import DeleteModal from "@/components/DeleteModal.vue";

const studenti = ref([]);
const studentToDelete = ref(null);
const router = useRouter();
const confirmModalRef = ref(null);

const fetchStudenti = async () => {
  try {
    const response = await axios.get("/api/studenti");
    studenti.value = response.data;
  } catch (error) {
    toast.error(error.response.data.message || error.message);
  }
};

const confirmDelete = (student) => {
  studentToDelete.value = student;
  confirmModalRef.value.showModal();
};

const deleteStudent = async () => {
  try {
    const response = await axios.delete(
      `/api/student-brisanje/${studentToDelete.value.id}`
    );
    studenti.value = studenti.value.filter(
      (student) => student.id !== studentToDelete.value.id
    );
    studentToDelete.value = null;
    confirmModalRef.value.hideModal();
    toast.success(response.data.message);
  } catch (error) {
    toast.error(error.response.data.message || error.message);
  }
};

onMounted(() => {
  fetchStudenti();
});
</script>

<template>
  <TableContainer to="/student-novi" buttonText="Dodaj studenta">
    <template #table-header>
      <tr>
        <th scope="col">Broj indeksa</th>
        <th scope="col">Ime</th>
        <th scope="col">Prezime</th>
        <th scope="col">Godina studija</th>
        <th scope="col">ESPB</th>
        <th scope="col">Prosek ocena</th>
        <th scope="col">Akcije</th>
      </tr>
    </template>
    <template #table-body>
      <tr v-for="student in studenti" :key="student.id">
        <td>
          <RouterLink :to="`/student/${student.id}`">{{
            student.broj_indeksa
          }}</RouterLink>
        </td>
        <td>{{ student.ime }}</td>
        <td>{{ student.prezime }}</td>
        <td>{{ student.godina_studija }}</td>
        <td>{{ student.espb }}</td>
        <td>{{ student.prosek_ocena }}</td>
        <td>
          <button
            @click="router.push(`/student-izmena/${student.id}`)"
            role="button"
            class="text-warning mx-1 btn btn-link"
          >
            <i class="fas fa-edit"></i>
          </button>
          <button
            @click="confirmDelete(student)"
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
    :message="'Da li ste sigurni da želite da obrišete studenta?'"
    :onConfirm="deleteStudent"
  />
</template>
