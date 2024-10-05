<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRoute, useRouter } from "vue-router";
import DeleteModal from "@/components/DeleteModal.vue";
import { toast } from "vue3-toastify";

// Modali
const studentToDelete = ref(null);
const ocenaToDelete = ref(null);
const confirmStudentModalRef = ref(null);
const confirmOcenaModalRef = ref(null);

const route = useRoute();
const router = useRouter();

// Student ID
const id = route.params.id;

const student = ref({});
const predmeti = ref([]);
const ocene = ref([]);
const ocena = ref("");
const predmetId = ref("");
const datum = ref("");

const fetchStudent = async () => {
  try {
    const response = await axios.get(`/api/student/${id}`);
    student.value = response.data.student;
    predmeti.value = response.data.predmeti;
    ocene.value = response.data.ocene;
  } catch (error) {
    if (error.response.status == 401) {
      router
        .push("/login")
        .then(() => toast.error(error.response.data.message || error.message));
    } else {
      toast.error(error.response.data.message || error.message);
    }
  }
};

const handleOcenaSubmit = async (event) => {
  event.preventDefault();
  try {
    const response = await axios.post(`/api/ocene`, {
      predmet_id: predmetId.value,
      student_id: id,
      ocena: ocena.value,
      datum: datum.value,
    });
    toast.success(response.data.message);
    await fetchStudent();
  } catch (error) {
    if (error.response.status == 401) {
      router
        .push("/login")
        .then(() => toast.error(error.response.data.message || error.message));
    } else {
      toast.error(error.response.data.message || error.message);
    }
  }
};

const confirmDeleteStudent = (student) => {
  studentToDelete.value = student;
  confirmStudentModalRef.value.showModal();
};

const confirmDeleteOcena = (ocena) => {
  ocenaToDelete.value = ocena;
  confirmOcenaModalRef.value.showModal();
};

const deleteStudent = async () => {
  try {
    const id = studentToDelete.value.id;
    const response = await axios.post(`/api/student-brisanje/${id}`);
    router.push("/studenti").then(() => toast.success(response.data.message));
  } catch (error) {
    if (error.response.status == 401) {
      router
        .push("/login")
        .then(() => toast.error(error.response.data.message || error.message));
    } else {
      toast.error(error.response.data.message || error.message);
    }
  }
};

const deleteOcena = async () => {
  try {
    const ocenaId = ocenaToDelete.value.id;
    const response = await axios.delete(`/api/ocene/${id}/${ocenaId}`);
    toast.success(response.data.message);
    await fetchStudent();
  } catch (error) {
    if (error.response.status == 401) {
      router
        .push("/login")
        .then(() => toast.error(error.response.data.message || error.message));
    } else {
      toast.error(error.response.data.message || error.message);
    }
  }
};

onMounted(() => {
  fetchStudent();
});
</script>

<template>
  <div class="container">
    <div class="row my-5">
      <div class="col-xs-12 col-md-6">
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
              <td>
                {{ new Date(student.datum_rodjenja).toLocaleDateString() }}
              </td>
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
                  @click="confirmDeleteStudent(student)"
                  class="text-danger mx-1 btn btn-link"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="col-xs-12 col-md-6">
        <form @submit="handleOcenaSubmit">
          <div class="form-group">
            <label for="predmet">Predmet</label>
            <select
              class="form-control"
              id="predmet"
              v-model="predmetId"
              required
            >
              <option
                v-for="predmet in predmeti"
                :key="predmet.id"
                :value="predmet.id"
              >
                {{ predmet.naziv }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="ocena">Ocena</label>
            <input
              type="number"
              class="form-control"
              id="ocena"
              v-model="ocena"
              required
            />
          </div>
          <div class="form-group">
            <label for="datum">Datum</label>
            <input
              type="date"
              class="form-control"
              id="datum"
              v-model="datum"
              required
            />
          </div>
          <button type="submit" class="btn btn-primary mt-4">Sačuvaj</button>
        </form>
      </div>
    </div>
    <div class="row justify-content-center">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">Šifra predmeta</th>
            <th scope="col">Naziv predmeta</th>
            <th scope="col">Godina</th>
            <th scope="col">ESPB</th>
            <th scope="col">Status predmeta</th>
            <th scope="col">Ocena</th>
            <th scope="col">Akcije</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="ocena in ocene" :key="ocena.id">
            <td>{{ ocena.sifra }}</td>
            <td>{{ ocena.naziv }}</td>
            <td>{{ ocena.godina_studija }}</td>
            <td>{{ ocena.espb }}</td>
            <td>{{ ocena.obavezni_izborni }}</td>
            <td>{{ ocena.ocena }}</td>
            <td>
              <a
                @click="confirmDeleteOcena(ocena)"
                class="icon-btn text-danger"
                role="button"
              >
                <i class="fas fa-trash-alt"></i>
              </a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <DeleteModal
      ref="confirmStudentModalRef"
      :title="'Potvrda brisanja'"
      :message="'Da li ste sigurni da želite da obrišete studenta?'"
      :onConfirm="deleteStudent"
    />
    <DeleteModal
      ref="confirmOcenaModalRef"
      :title="'Potvrda brisanja'"
      :message="'Da li ste sigurni da želite da obrišete ocenu?'"
      :onConfirm="deleteOcena"
    />
  </div>
</template>
