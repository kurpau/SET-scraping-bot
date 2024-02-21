<template>
  <div class="container">
    <div class="header">
      <div data-label="Name">
        <a target=”_blank” :href="stock.url">{{ stock.name }}</a>
      </div>
      <div data-label="Tikcer">{{ stock.symbol }}</div>
    </div>
    <hr />
    <div class="details">
      <div>
        <div data-label="Date">{{ parsedDate }}</div>
      </div>
      <div class="eps">
        <div class="period">
          <div class="labeled">
            <label>Current</label>
            <span data-label="EPScurr">{{ stock.eps[0].toFixed(2) }}</span>
          </div>
          <div class="labeled">
            <label>Previous</label>
            <span data-label="EPSprev">{{ stock.eps[1].toFixed(2) }}</span>
          </div>
        </div>
        <div class="change">
          <div class="labeled">
            <label>Growth</label>
            <div>
              <span :class="{ 'eps-green': epsChange > 0, 'eps-red': epsChange < 0 }">{{ epsChange.toFixed(2) }}</span>
              <span v-if="epsChange > 0" class="material-symbols-outlined">
                arrow_upward
              </span>
              <span v-else class="material-symbols-outlined">
                arrow_downward
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, } from "vue";
const props = defineProps(["stock"]);

const strDate = ref(props.stock.date);

const epsChange = computed(() => props.stock.eps[0] - props.stock.eps[1]);
const parsedDate = computed(() => {
  const date = new Date(strDate.value);

  // Extract the parts of the date
  const year = date.getFullYear();
  const month = (date.getMonth() + 1).toString().padStart(2, "0"); // Months are  0-indexed
  const day = date.getDate().toString().padStart(2, "0");
  const hour = date.getHours().toString().padStart(2, "0");
  const minute = date.getMinutes().toString().padStart(2, "0");

  return `${year}-${month}-${day} ${hour}:${minute}`;
});
</script>

<style scoped>
.container {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  padding: 1rem;
  margin: 0.8rem auto;
  width: 100%;
}

.header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

a {
  color: black;
  text-decoration: none;
  text-transform: uppercase;
}

a:hover {
  cursor: pointer;
}

.details {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.eps-red {
  color: red;
}

.eps-green {
  color: green;
}

.eps {
  display: flex;
  flex-direction: row;
  gap: 5rem;
}

.period {
  display: flex;
  gap: 5rem;
}

.labeled {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.labeled div {
  display: flex;
  justify-items: center;
}

.change {
  display: flex;
  align-items: center;
}
</style>
