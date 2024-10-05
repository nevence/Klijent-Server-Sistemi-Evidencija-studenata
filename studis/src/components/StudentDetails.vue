<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import DeleteModal from "./DeleteModal.vue";
import { toast } from "vue3-toastify";

const router = useRouter();

const studentToDelete = ref(null);
const confirmModalRef = ref(null);

const confirmDelete = (student) => {
  studentToDelete.value = student;
  confirmModalRef.value.showModal();
};

const deleteStudent = async () => {
  try {
    const id = studentToDelete.value.id;
    const response = await axios.delete(`/api/student-brisanje/${id}`);
    router.push("/studenti").then(() => toast.success(response.data.message));
  } catch (error) {
      toast.error(error.response.data.message || error.message);
    }
  }
};

defineProps({
  student: Object,
});
</script>

<template>
  <div>
    <table class="table">
      <tbody>
        <tr>
          <th>Ime</th>
          <td>{{ student.ime }}</td>
        </tr>
        <tr>
          <th>Ime roditelja</th>
          <td>{{ student.ime_roditelja }}</td>
        </tr>
        <tr>
          <th>Prezime</th>
          <td>{{ student.prezime }}</td>
        </tr>
        <tr>
          <th>Broj indeksa</th>
          <td>{{ student.broj_indeksa }}</td>
        </tr>
        <tr>
          <th>Godina studija</th>
          <td>{{ student.godina_studija }}</td>
        </tr>
        <tr>
          <th>Broj telefona</th>
          <td>{{ student.broj_telefona }}</td>
        </tr>
        <tr>
          <th>Email</th>
          <td>{{ student.email }}</td>
        </tr>
        <tr>
          <th>Datum rođenja</th>
          <td>{{ new Date(student.datum_rodjenja).toLocaleDateString() }}</td>
        </tr>
        <tr>
          <th>JMBG</th>
          <td>{{ student.jmbg }}</td>
        </tr>
        <tr>
          <th>Ukupno ESPB</th>
          <td>{{ student.espb }}</td>
        </tr>
        <tr>
          <th>Prosek ocena</th>
          <td>{{ student.prosek_ocena }}</td>
        </tr>
        <tr>
          <th>Akcije</th>
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
      </tbody>
    </table>
    <DeleteModal
      ref="confirmModalRef"
      :title="'Potvrda brisanja'"
      :message="'Da li ste sigurni da želite da obrišete studenta?'"
      @confirm="deleteStudent"
    />
  </div>
</template>
