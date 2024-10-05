<script setup>
import { defineProps } from "vue";

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <div class="container">
    <div class="row">
      <div class="col-lg-6 col-12">
        <div class="my-5">
          <h3>{{ title }}</h3>
        </div>
        <slot></slot>
      </div>
    </div>
  </div>
</template>
