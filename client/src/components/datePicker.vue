<template>
  <div class="container">
    <base-button @click="setDateRange('today')">Today</base-button>
    <base-button @click="setDateRange('5D')">5D</base-button>
    <base-button @click="setDateRange('1M')">1M</base-button>
    <base-button @click="setDateRange('3M')">3M</base-button>
  </div>
  <div class="date-container">
    <label for="start">Start date:</label>
    <input
      type="date"
      id="start"
      v-model="startDate"
      :max="today"
      @change="emitDateUpdate"
    />

    <label for="end">End date:</label>
    <input
      type="date"
      id="end"
      v-model="endDate"
      :max="today"
      @change="emitDateUpdate"
    />
  </div>
</template>

<script setup>
import { ref } from "vue";

const emit = defineEmits(["update-dates"]);

function formatDate(date) {
  return date.toISOString().substring(0, 10);
}

const today = formatDate(new Date());
const startDate = ref(today);
const endDate = ref(today);

function setDateRange(period) {
  const today = new Date();
  let start = new Date();

  switch (period) {
    case "today":
      start = today;
      break;
    case "5D":
      start.setDate(today.getDate() - 5);
      break;
    case "1M":
      start.setMonth(today.getMonth() - 1);
      break;
    case "3M":
      start.setMonth(today.getMonth() - 3);
      break;
    default:
      throw new Error(`Unknown period: ${period}`);
  }

  startDate.value = formatDate(start);
  endDate.value = period === "today" ? startDate.value : formatDate(today);
  emitDateUpdate();
}

function emitDateUpdate() {
  emit("update-dates", { start: startDate.value, end: endDate.value });
}
</script>

<style scoped>
.container {
  gap: 10px;
  display: flex;
}
</style>
