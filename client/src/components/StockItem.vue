<template>
  <div class="container">
    <base-card>
      <div data-label="Name">
        <a :href="stock.url">{{ stock.name }}</a>
      </div>
      <hr />
      <div class="details">
        <div>
          <div data-label="Tikcer">{{ stock.symbol }}</div>
        </div>
        <div class="eps">
          <div class="period">
            <span data-label="EPScurr">{{ stock.eps[0] }}</span>
            <span data-label="EPSprev">{{ stock.eps[1] }}</span>
          </div>
          <div class="change">
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
    </base-card>
  </div>
</template>

<script setup>
import { computed } from "vue";
const props = defineProps(["stock"]);

const epsChange = computed(() => props.stock.eps[0] - props.stock.eps[1]);
</script>

<style scoped>
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

.change {
  display: flex;
  align-items: center;
}
</style>
