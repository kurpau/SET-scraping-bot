<template>
  <div class="container">
    <div class="header">
      <div>
        <a target=”_blank” :href="stock.url">{{ stock.name }}</a>
      </div>
      <div>{{ stock.symbol }}</div>
    </div>
    <hr />
    <div class="details">
      <div id='report-date' data-label="Date">{{ parsedDate }}</div>
      <div class="eps">
        <div class="labeled">
          <p>Current</p>
          <span data-label="EPScurr">{{ stock.eps[0].toFixed(2) }}</span>
        </div>
        <div class="labeled">
          <p>Previous</p>
          <span data-label="EPSprev">{{ stock.eps[1].toFixed(2) }}</span>
        </div>
        <div class="labeled">
          <p>Growth</p>
          <div>
            <span :class="{ 'eps-green': epsChange > 0, 'eps-red': epsChange < 0 }">{{
              epsChange.toFixed(2) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
const props = defineProps(["stock"]);

const epsChange = computed(() => props.stock.eps[0] - props.stock.eps[1]);
const parsedDate = computed(() => {
  const parsedDate = new Date(props.stock.date);

  const hour = parsedDate.getUTCHours().toString().padStart(2, "0");
  const minute = parsedDate.getUTCMinutes().toString().padStart(2, "0");

  return `${hour}:${minute}`;
});
</script>

<style scoped>
.container {
  border-radius: 12px;
  box-shadow: 0 2px 8px var(--card-shadow);
  padding: 1rem;
  margin: 0.5rem auto;
  width: 100%;
}

.header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
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
  gap: 5rem;
}

#report-date {
  text-align: center;
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

.labeled p {
  margin: 0;
}

.labeled div {
  display: flex;
  justify-items: center;
}

.change {
  display: flex;
  align-items: center;
}

@media (max-width: 600px) {

  .header,
  .details,
  .eps {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
