<template>
  <div class="container">
    <base-button>Today</base-button>
    <base-button>Yesterday</base-button>
    <base-button>Last 5 days</base-button>
    <base-button @click="fetchStocks">Last month</base-button>
    <base-button>Last 3 months</base-button>
    <base-button>Fetch Stocks</base-button>
  </div>
  <div class="date-container">
    <label for="start">Start date:</label>
    <input type="date" id="start" v-model="startDate" />

    <label for="end">End date:</label>
    <input type="date" id="end" v-model="endDate" />
  </div>
  <stock-list :stocks="stocks"></stock-list>
  {{ stocks }}
</template>

<script setup>
import { ref } from "vue";
import StockList from "../components/StockList.vue";

function formatTodayDate() {
  const today = new Date();
  return today.toISOString().substring(0, 10);
}

const stocks = ref([]);
const startDate = ref(formatTodayDate());
const endDate = ref(formatTodayDate());

async function fetchStocks() {
  const path = `http://localhost:5000/stocks?from=${startDate.value}&to=${endDate.value}`;
  const res = await fetch(path);
  const data = await res.json();
  stocks.value = [...data.stocks];
}
</script>

<style scoped>
.container {
  gap: 10px;
  display: flex;
}
</style>
