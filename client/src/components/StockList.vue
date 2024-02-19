<template>
  <base-card>
    <div class="info" v-if="isLoading">
      <base-spinner></base-spinner>
    </div>
    <div v-else>
      <div class="results" v-if="stocks">
        <caption>
          Fetch Results
        </caption>
        <stock-item
          v-for="stock in stocks"
          :key="stock.id"
          :stock="stock"
        ></stock-item>
      </div>
      <div class="info" v-else>
        <p>
          Select a date range and click 'Fetch Stocks' to see the latest stock
          information.
        </p>
      </div>
    </div>
  </base-card>
</template>

<script setup>
import StockItem from "./StockItem.vue";
defineProps(["stocks", "isLoading"]);
</script>

<style scoped>
.info {
  display: flex;
  justify-content: center;
  align-items: center;
}

.results {
  display: flex;
  flex-direction: column;
  justify-items: center;
}

caption {
  font-size: 1.5em;
  font-weight: 800;
  margin-top: 1rem;
}
</style>
