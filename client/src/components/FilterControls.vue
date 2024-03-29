<template>
  <div class="filters">
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
    <div>
      <base-button @click="resetFilters">Reset</base-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";

const emit = defineEmits(["filters-changed"]);

const sorting = useLocalStorage("sorting", "desc");
const epsFilter = useLocalStorage("epsFilter", "");
const activeSearchTerm = useLocalStorage("activeSearchTerm", "");
const onlyPositive = useLocalStorage("onlyPositive", false);
const sortBy = useLocalStorage("sortBy", "date");

function useLocalStorage(key, defaultValue) {
  const data = ref(defaultValue);

  onMounted(() => {
    const storedValue = localStorage.getItem(key);
    if (storedValue !== null) {
      data.value = JSON.parse(storedValue);
    }
  });

  watch(data, (newValue) => {
    localStorage.setItem(key, JSON.stringify(newValue));
  });

  return data;
}

function sort(mode) {
  sorting.value = mode;
}


function resetFilters() {
  sorting.value = "desc";
  epsFilter.value = "";
  activeSearchTerm.value = "";
  onlyPositive.value = false;
  sortBy.value = "date";
}

const emitFilterChange = () => {
  emit("filters-changed", {
    sorting: sorting.value,
    epsFilter: epsFilter.value,
    activeSearchTerm: activeSearchTerm.value,
    onlyPositive: onlyPositive.value,
    sortBy: sortBy.value
  });
};

watch([sorting, epsFilter, activeSearchTerm, onlyPositive, sortBy], emitFilterChange, { deep: true });

</script>

<style scoped>
.filters {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
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

@media (max-width: 768px) {

  .filters,
  .sort,
  .text-input {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
