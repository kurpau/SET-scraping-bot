<template>
  <div class="container">
    <base-button>Today</base-button>
    <base-button>Yesterday</base-button>
    <base-button>Last 5 days</base-button>
    <base-button @click="fetchStocks">Last month</base-button>
    <base-button>Last 3 months</base-button>
  </div>
  <stock-list :stocks="stocks"></stock-list>
</template>

<script setup>
import { ref } from "vue";
import StockList from "../components/StockList.vue";

const stocks = ref([]);

async function fetchStocks() {
  const path = "http://localhost:5000/stocks?from=2023-12-27&to=2024-01-27";
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
