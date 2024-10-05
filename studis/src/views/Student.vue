<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRoute, useRouter } from "vue-router";
import StudentDetails from "@/components/StudentDetails.vue";
import OcenaForm from "@/components/OcenaForm.vue";
import OcenaList from "@/components/OcenaList.vue";
import { toast } from "vue3-toastify";

const route = useRoute();
const router = useRouter();

const id = route.params.id;

const student = ref({});
const predmeti = ref([]);
const ocene = ref([]);

const fetchStudent = async () => {
  try {
    const response = await axios.get(`/api/student/${id}`);
    student.value = response.data.student;
    predmeti.value = response.data.predmeti;
    ocene.value = response.data.ocene;
  } catch (error) {
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
        <StudentDetails :student="student" />
      </div>
      <div class="col-xs-12 col-md-6">
        <OcenaForm
          :predmeti="predmeti"
          :studentId="parseInt(id)"
          @ocenaAdded="fetchStudent"
        />
      </div>
    </div>
    <div class="row justify-content-center">
      <OcenaList
        :ocene="ocene"
        :studentId="parseInt(id)"
        @ocenaDeleted="fetchStudent"
      />
    </div>
  </div>
</template>
