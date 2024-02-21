<template>
  <base-card>
    <div class="info" v-if="isLoading">
      <base-spinner></base-spinner>
    </div>
    <div v-else>
      <div class="results" v-if="stocks">
        <div class='header'>
          <caption>
            Fetch Results
          </caption>
          <div class='controls'></div>
          <base-button @click="sort('asc')" :class="{ selected: sorting === 'asc' }">
            Sort Ascending
          </base-button>
          <base-button @click="sort('desc')" :class="{ selected: sorting === 'desc' }">
            Sort Descending
          </base-button>
          <input type='number' step="0.01" v-model="epsFilter" placeholder="Filter by EPS" />
          <input type='text' v-model="activeSearchTerm" placeholder="Filter by Name" />
          <br>
          <label>Only positive EPS</label>
          <input type="checkbox" v-model="onlyPositive">
        </div>
        <hr>
        <stock-item v-for="stock in displayedStocks" :key="stock.id" :stock="stock"></stock-item>
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
import { ref, computed } from "vue";
const props = defineProps(["fetchedStocks", "isLoading"]);

const sorting = ref(null);
const stocks = computed(() => props.fetchedStocks);
const epsFilter = ref();
const activeSearchTerm = ref("");
const onlyPositive = ref(false);

function sort(mode) {
  sorting.value = mode;
}

const displayedStocks = computed(() => {
  let modifiedStocks = stocks.value;

  modifiedStocks = modifiedStocks.sort((i1, i2) => {
    const i1Growth = i1.eps[0] - i1.eps[1];
    const i2Growth = i2.eps[0] - i2.eps[1];
    if (sorting.value === "asc") {
      return i1Growth - i2Growth;
    } else if (sorting.value === "desc") {
      return i2Growth - i1Growth;
    }
  });

  if (epsFilter.value !== "") {
    modifiedStocks = modifiedStocks.filter((stock) => (stock.eps[0] - stock.eps[1]) >= epsFilter.value);
  }

  if (activeSearchTerm.value !== "") {
    modifiedStocks = modifiedStocks.filter((stock) =>
      stock.name.toLowerCase().includes(activeSearchTerm.value.toLowerCase()) || stock.symbol.toLowerCase().includes(activeSearchTerm.value.toLowerCase())
    );
  }

  if (onlyPositive.value) {
    modifiedStocks = modifiedStocks.filter((stock) =>
      stock.eps[0] >= 0 && stock.eps[1] >= 0
    );
  }

  return modifiedStocks;
});

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

.header {
  margin: 0 auto;
}

hr {
  width: 100%
}

caption {
  font-size: 1.5em;
  font-weight: 800;
  margin: 0.5rem auto;
  white-space: nowrap;
}
</style>
