<template>
  <base-card>
    <!-- TODO -->
    <!-- make error dialog/window -->
    <!-- make responsive for mobile -->
    <!-- default prop value for stocks?  -->
    <!-- remember to handle errors in backend -->
    <!-- check for duplicate stocks because of SET pagination.... -->
    <!-- commnent the code -->
    <!-- clean up the stocks list file -->
    <div class="info" v-if="isLoading">
      <base-spinner></base-spinner>
    </div>
    <div v-else>
      <div class="results" v-if="displayedStocks">
        <div class='header'>
          <div>
            <caption>
              Fetch Results ({{ displayedStocks.length }})
            </caption>
          </div>
          <div class='controls'></div>
          <div class="sort">
            <div>
              <label>Sort by:
                <select name="select-sort" v-model="sortBy">
                  <option value="date">Date</option>
                  <option value="growth">Growth</option>
                </select>
              </label>
            </div>
            <base-button @click="sort('desc')" :class="{ selected: sorting === 'desc' }">
              Descending
            </base-button>
            <base-button @click="sort('asc')" :class="{ selected: sorting === 'asc' }">
              Ascending
            </base-button>
          </div>
          <div class='text-input'>
            <input name="growth-threshold" type='number' step="0.01" v-model="epsFilter" placeholder="Growth Threshold" />
            <input name="name-filter" type='text' v-model="activeSearchTerm" placeholder="Filter by Name" />
          </div>
          <div>
            <label for='positive-eps'>Only Positive EPS</label>
            <input type="checkbox" id='positive-eps' v-model="onlyPositive">
          </div>
        </div>
        <hr>
        <p v-if="displayedStocks.length === 0">No results found for these filters</p>
        <stock-item v-else v-for="stock in displayedStocks" :key="stock.id" :stock="stock"></stock-item>
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
import { ref, computed, onMounted, watch } from "vue";
const props = defineProps(["fetchedStocks", "isLoading"]);

const sorting = useLocalStorage("sorting", "desc");
const epsFilter = useLocalStorage("epsFilter", "");
const activeSearchTerm = useLocalStorage("activeSearchTerm", "");
const onlyPositive = useLocalStorage("onlyPositive", false);
const sortBy = useLocalStorage("sortBy", "date");


function sort(mode) {
  sorting.value = mode;
}

const displayedStocks = computed(() => {
  let modifiedStocks = props.fetchedStocks && props.fetchedStocks?.length > 0 ? [...props.fetchedStocks] : JSON.parse(localStorage.getItem("stocksData") || "[]");

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

// Helper function to sync state with local storage
function useLocalStorage(key, defaultValue) {
  const data = ref(defaultValue);

  // Load initial state from local storage or use default
  onMounted(() => {
    const storedValue = localStorage.getItem(key);
    if (storedValue !== null) {
      data.value = JSON.parse(storedValue);
    }
  });

  // Watch for changes and update local storage
  watch(data, (newValue) => {
    localStorage.setItem(key, JSON.stringify(newValue));
  });

  return data;
}


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

.sort {
  display: flex;
  align-items: center;
  gap: 10px;
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
