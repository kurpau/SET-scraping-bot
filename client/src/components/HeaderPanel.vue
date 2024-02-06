<template>
  <base-card>
    <div class="container">
      <date-picker @update-dates="handleDateUpdate"></date-picker>
      <base-button id="fetch-button" @click="fetchStocks"
        >Fetch Stocks</base-button
      >
    </div>
  </base-card>
</template>

<script setup>
import DatePicker from "./DatePicker.vue";

import { ref } from "vue";
import { useRouter } from "vue-router";

const emit = defineEmits(["fetchStocks"]);
const router = useRouter();
const startDate = ref("");
const endDate = ref("");

function handleDateUpdate({ start, end }) {
  startDate.value = start;
  endDate.value = end;
  router.push({ path: "/", query: { fromDate: start, toDate: end } });
}

async function fetchStocks() {
  const path = `http://localhost:5000/stocks?from=${startDate.value}&to=${endDate.value}`;
  const res = await fetch(path);
  const data = await res.json();

  emit("fetchStocks", [...data.stocks]);
}
</script>

<style scoped>
#fetch-button {
  display: block;
  margin-left: auto;
  margin-right: 0;
}
</style>
