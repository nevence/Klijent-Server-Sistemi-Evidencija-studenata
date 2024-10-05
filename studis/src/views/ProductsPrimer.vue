<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { toast } from "vue3-toastify";

const products = ref([]); // Ref (reaktivna promenljiva) za čuvanje liste proizvoda

const fetchProducts = async () => {
  try {
    const response = await axios.get("api/products"); // Poziv Flask API-ja
    products.value = response.data; // Čuvanje podataka u products ref
  } catch (error) {
    toast.error("Greška pri preuzimanju proizvoda: " + error.message);
  }
};

onMounted(() => {
  /* Poziv API-ja kada se komponenta mount-uje
 (Dodavanje HTML elemenata koji odgovaraju ovoj komponenti u DOM) */
  fetchProducts();
});
</script>

<template>
  <div>
    <h1>Lista proizvoda</h1>
    <ul>
      <li v-for="product in products" :key="product.id">
        {{ product.name }} - Cena: {{ product.price }} RSD
      </li>
    </ul>
  </div>
</template>

<style>
/* Stilovi po želji */
</style>
