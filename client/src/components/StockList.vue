<template>
  <base-card>
    <!-- TODO -->
    <!-- make error dialog/window -->
    <!-- make responsive for mobile -->
    <!-- export option to csv/excel? -->
    <!-- handle errors in backend -->
    <!-- commnent the code -->
    <!-- handle server timeouts or no reports -->
    <div class="info" v-if="isLoading">
      <base-spinner></base-spinner>
    </div>
    <div v-else-if='isError'>
      <div class='info'>
        <p style="color: red;">Something went wrong, try fetching again!</p>
      </div>
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
    type: Array,
    default: () => [],
    required: true,
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
  isError: {
    type: Boolean,
    default: false,
  }
});

// Reactive state for filters
const filters = reactive({
  sorting: "desc",
  epsFilter: "",
  activeSearchTerm: "",
  onlyPositive: false,
  sortBy: "date",
});

// Function to handle filter changes
function handleFiltersChanged(newFilters) {
  Object.assign(filters, newFilters);
}

// Helper functions for readability and modularity
function sortStocks(stocks) {
  return stocks.sort((a, b) => {
    if (filters.sortBy === "growth") {
      const growthA = a.eps[0] - a.eps[1];
      const growthB = b.eps[0] - b.eps[1];
      return filters.sorting === "asc" ? growthA - growthB : growthB - growthA;
    }
    // Default to sorting by date
    const dateA = new Date(a.date), dateB = new Date(b.date);
    return filters.sorting === "asc" ? dateA - dateB : dateB - dateA;
  });
}

function filterStocks(stocks) {
  return stocks.filter(stock => {
    const growth = stock.eps[0] - stock.eps[1];
    const matchesEpsFilter = filters.epsFilter === "" || growth >= filters.epsFilter;
    const matchesSearchTerm = filters.activeSearchTerm === "" || stock.name.toLowerCase().includes(filters.activeSearchTerm.toLowerCase()) || stock.symbol.toLowerCase().includes(filters.activeSearchTerm.toLowerCase());
    const isPositive = !filters.onlyPositive || (stock.eps[0] >= 0 && stock.eps[1] >= 0);
    return matchesEpsFilter && matchesSearchTerm && isPositive;
  });
}

// Computed property to fetch or retrieve stocks
const stocks = computed(() => {
  return props.fetchedStocks && props.fetchedStocks?.length > 0 ? [...props.fetchedStocks] : JSON.parse(localStorage.getItem("stocksData") || "[]");
});

// Displayed stocks based on filters
const displayedStocks = computed(() => {
  let modifiedStocks = [...stocks.value];
  modifiedStocks = sortStocks(stocks.value);
  modifiedStocks = filterStocks(modifiedStocks);
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
