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
          <div>
            <caption>
              Fetch Results ({{ displayedStocks.length }})
            </caption>
            <!--  need to add events -->
            <filter-controls />
            ha
          </div>
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
import { computed } from "vue";
const props = defineProps({
  fetchedStocks: {
    required: true,
    default: () => [],
    type: Array,
  }, isLoading: { type: Boolean },
});



const stocks = computed(() => props.fetchedStocks && props.fetchedStocks?.length > 0 ? [...props.fetchedStocks] : JSON.parse(localStorage.getItem("stocksData") || "[]"));


const displayedStocks = computed(() => {
  let modifiedStocks = [...stocks.value];

  modifiedStocks = modifiedStocks.sort((i1, i2) => {
    if (sortBy.value === "growth") {
      const i1Growth = i1.eps[0] - i1.eps[1];
      const i2Growth = i2.eps[0] - i2.eps[1];
      if (sorting.value === "asc") {
        return i1Growth - i2Growth;
      } else if (sorting.value === "desc") {
        return i2Growth - i1Growth;
      }
    } else if (sortBy.value === "date") {
      if (sorting.value === "asc") {
        return new Date(i1.date) - new Date(i2.date);
      } else if (sorting.value === "desc") {
        return new Date(i2.date) - new Date(i1.date);
      }
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
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
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

.text-input {
  display: flex;
  gap: 10px;
}

.text-input input {
  padding: 5px 12px;
  font-size: 16px;
  line-height: 20px;
  color: var(--color-text);
  vertical-align: middle;
  background-color: transparent;
  background-repeat: no-repeat;
  background-position: right 8px center;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  outline: none;
}

.text-input input:focus {
  /* prevent shift on focus */
  padding: 4px 11px;
  outline: none;
  border: 2px solid var(--color-accent-fg)
}
</style>
