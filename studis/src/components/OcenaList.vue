<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { toast } from "vue3-toastify";
import DeleteModal from "@/components/DeleteModal.vue";

const props = defineProps({
  ocene: Array,
  studentId: Number,
});

const emit = defineEmits(["ocenaDeleted"]);

const ocenaToDelete = ref(null);
const confirmModalRef = ref(null);

const router = useRouter();

const confirmDelete = (ocena) => {
  ocenaToDelete.value = ocena;
  confirmModalRef.value.showModal();
};

const deleteOcena = async () => {
  try {
    const ocenaId = ocenaToDelete.value.id;
    const response = await axios.delete(
      `/api/ocene/${props.studentId}/${ocenaId}`
    );
    toast.success(response.data.message);
    emit("ocenaDeleted");
  } catch (error) {
      toast.error(error.response.data.message || error.message);
    }
  }
};
</script>

<template>
  <div>
    <table class="table mt-5">
      <thead>
        <tr>
          <th>Predmet</th>
          <th>Ocena</th>
          <th>Datum</th>
          <th>Akcije</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ocena in ocene" :key="ocena.id">
          <td>{{ ocena.naziv }}</td>
          <td>{{ ocena.ocena }}</td>
          <td>{{ new Date(ocena.datum).toLocaleDateString() }}</td>
          <td>
            <button
              @click="confirmDelete(ocena)"
              class="btn btn-outline-danger"
              role="button"
            >
              <i class="fas fa-trash-alt"></i>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <DeleteModal
      ref="confirmModalRef"
      :title="'Potvrda brisanja'"
      :message="'Da li ste sigurni da želite da obrišete ocenu?'"
      @confirm="deleteOcena"
    />
  </div>
</template>
