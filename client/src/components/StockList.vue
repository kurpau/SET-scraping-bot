<template>
  <base-card>
    <!-- TODO -->
    <!-- normalize colors <br> -->
    <!-- normalize fonts <br> -->
    <!-- make responsive for mobile -->
    <!-- make error dialog/window -->
    <div class="info" v-if="isLoading">
      <base-spinner></base-spinner>
    </div>
    <div v-else>
      <div class="results" v-if="stocks">
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
              Sort Descending
            </base-button>
            <base-button @click="sort('asc')" :class="{ selected: sorting === 'asc' }">
              Sort Ascending
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

const sorting = ref("desc");
const stocks = computed(() => props.fetchedStocks);
const epsFilter = ref("");
const activeSearchTerm = ref("");
const onlyPositive = ref(false);
const sortBy = ref("date");

function sort(mode) {
  sorting.value = mode;
}

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
  width: 100%
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
  color: #24292e;
  vertical-align: middle;
  background-color: #ffffff;
  background-repeat: no-repeat;
  background-position: right 8px center;
  border: 1px solid #e1e4e8;
  border-radius: 6px;
  outline: none;
  box-shadow: rgba(225, 228, 232, 0.2) 0px 1px 0px 0px inset;
}

.text-input input:focus {
  border-color: #0366d6;
  outline: none;
  box-shadow: rgba(3, 102, 214, 0.3) 0px 0px 0px 3px;
}
</style>
