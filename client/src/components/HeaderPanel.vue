<template>
  <base-card>
    <date-picker @update-dates="handleDateUpdate"></date-picker>
    <base-button @click="fetchStocks">Fetch Stocks</base-button>
  </base-card>
</template>

<script setup>
import DatePicker from "./DatePicker.vue";

import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const stocks = ref([]);
const startDate = ref("");
const endDate = ref("");

function handleDateUpdate({ start, end }) {
  startDate.value = start;
  endDate.value = end;
  router.push({ path: "/", query: { fromDate: start, toDate: end } });
}

async function fetchStocks() {
  // Use the reactive start and end dates directly
  const path = `http://localhost:5000/stocks?from=${startDate.value}&to=${endDate.value}`;
  const res = await fetch(path);
  const data = await res.json();
  stocks.value = [...data.stocks];
}
</script>
