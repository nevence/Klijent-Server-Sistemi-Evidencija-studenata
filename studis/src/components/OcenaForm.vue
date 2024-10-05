<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { toast } from "vue3-toastify";

const props = defineProps({
  predmeti: Array,
  studentId: Number,
});

const emit = defineEmits(["ocenaAdded"]);

const ocena = ref("");
const predmetId = ref("");
const datum = ref("");

const router = useRouter();

const handleSubmit = async (event) => {
  event.preventDefault();
  try {
    const response = await axios.post(`/api/ocene`, {
      predmet_id: predmetId.value,
      student_id: props.studentId,
      ocena: ocena.value,
      datum: datum.value,
    });
    toast.success(response.data.message);
    emit("ocenaAdded");
  } catch (error) {
      toast.error(error.response.data.message || error.message);
    }
  }
};
</script>

<template>
  <form @submit="handleSubmit">
    <div class="form-group">
      <label for="predmet">Predmet</label>
      <select v-model="predmetId" class="form-control" id="predmet" required>
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
        v-model="ocena"
        type="number"
        class="form-control"
        id="ocena"
        required
      />
    </div>
    <div class="form-group">
      <label for="datum">Datum</label>
      <input
        v-model="datum"
        type="date"
        class="form-control"
        id="datum"
        required
      />
    </div>
    <button type="submit" class="btn btn-primary mt-4">Sačuvaj</button>
  </form>
</template>
