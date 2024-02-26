<template>
  <base-card>
    <!-- TODO -->
    <!-- clean up the stocks list file -->
    <!-- export some code to SortControls.vue -->
    <!-- make error dialog/window -->
    <!-- make responsive for mobile -->
    <!-- export option to csv/excel? -->
    <!-- handle errors in backend -->
    <!-- commnent the code -->
    <!-- handle server timeouts or no reports -->
    <div class="info" v-if="isLoading">
      <base-spinner></base-spinner>
    </div>
    <div v-else>
      <div class="info" v-if="stocks.length === 0">
        <p>
          Select a date range and click 'Fetch Stocks' to see the latest stock
          information.
        </p>
      </div>
      <div class="results" v-else>
        <div class='header'>
          <caption>
            Fetch Results ({{ displayedStocks.length }})
          </caption>
          <filter-controls @filters-changed="handleFiltersChanged" />
        </div>
        <hr>
        <div class='info' v-if="displayedStocks.length === 0">
          <p>No stocks meet the filter criteria.</p>
        </div>
        <stock-item v-else v-for="stock in displayedStocks" :key="stock.id" :stock="stock"></stock-item>
      </div>
    </div>
  </base-card>
</template>

<script setup>
import StockItem from "./StockItem.vue";
import FilterControls from "./FilterControls.vue";
import { reactive, computed } from "vue";

const props = defineProps({
  fetchedStocks: {
    required: true,
    default: () => [],
    type: Array,
  }, isLoading: { type: Boolean },
});

const filters = reactive({
  sorting: "desc",
  epsFilter: "",
  activeSearchTerm: "",
  onlyPositive: false,
  sortBy: "date"
});

function handleFiltersChanged(newFilters) {
  Object.assign(filters, newFilters);
}

const stocks = computed(() => props.fetchedStocks && props.fetchedStocks?.length > 0 ? [...props.fetchedStocks] : JSON.parse(localStorage.getItem("stocksData") || "[]"));


const displayedStocks = computed(() => {
  let modifiedStocks = [...stocks.value];

  modifiedStocks = modifiedStocks.sort((i1, i2) => {
    if (filters.sortBy === "growth") {
      const i1Growth = i1.eps[0] - i1.eps[1];
      const i2Growth = i2.eps[0] - i2.eps[1];
      if (filters.sorting === "asc") {
        return i1Growth - i2Growth;
      } else if (filters.sorting === "desc") {
        return i2Growth - i1Growth;
      }
    } else if (filters.sortBy === "date") {
      if (filters.sorting === "asc") {
        return new Date(i1.date) - new Date(i2.date);
      } else if (filters.sorting === "desc") {
        return new Date(i2.date) - new Date(i1.date);
      }
    }
  });

  if (filters.epsFilter !== "") {
    modifiedStocks = modifiedStocks.filter((stock) => (stock.eps[0] - stock.eps[1]) >= filters.epsFilter);
  }

  if (filters.activeSearchTerm !== "") {
    modifiedStocks = modifiedStocks.filter((stock) =>
      stock.name.toLowerCase().includes(filters.activeSearchTerm.toLowerCase()) || stock.symbol.toLowerCase().includes(filters.activeSearchTerm.toLowerCase())
    );
  }

  if (filters.onlyPositive) {
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
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

hr {
  width: 100%;
  margin: 20px 0 15px 0;
}

caption {
  font-size: 1.5em;
  font-weight: 600;
  margin-top: 10px;
  white-space: nowrap;
}
</style>
