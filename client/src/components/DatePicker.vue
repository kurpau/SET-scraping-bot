<template>
  <div class="container">
    <div class="period-buttons">
      <base-button @click="setDateRange('today')"
        :mode="activeRange === 'today' ? 'selected' : 'default'">Today</base-button>
      <base-button @click="setDateRange('5D')" :mode="activeRange === '5D' ? 'selected' : 'default'">5D</base-button>
      <base-button @click="setDateRange('1M')" :mode="activeRange === '1M' ? 'selected' : 'default'">1M</base-button>
      <base-button @click="setDateRange('3M')" :mode="activeRange === '3M' ? 'selected' : 'default'">3M</base-button>
    </div>
    <div class="date-picker">
      <div class="input-container">
        <label for="start" class="date-label">Start Date</label>
        <input type="date" id="start" class="date-input" v-model="startDate" :max="today" @change="emitDateUpdate" />
      </div>
      <div class="input-container">
        <label for="end" class="date-label">End Date</label>
        <input type="date" id="end" class="date-input" v-model="endDate" :max="today" @change="emitDateUpdate" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();

const emit = defineEmits(["update-dates"]);
const activeRange = ref("");

const formatDate = (date) => date.toISOString().substring(0, 10);

const today = formatDate(new Date());
const startDate = ref(route.query.fromDate || today);
const endDate = ref(route.query.toDate || today);

function setDateRange(period) {
    activeRange.value = period;
    const start = calculateStartDate(period);

    startDate.value = formatDate(start);
    endDate.value = period === "today" ? startDate.value : formatDate(new Date());
    emitDateUpdate();
}

function emitDateUpdate() {
    emit("update-dates", { start: startDate.value, end: endDate.value });
}

function calculateStartDate(period) {
    const today = new Date();
    switch (period) {
    case "today":
        return today;
    case "5D":
        return new Date(today.setDate(today.getDate() - 5));
    case "1M":
        return new Date(today.setMonth(today.getMonth() - 1));
    case "3M":
        return new Date(today.setMonth(today.getMonth() - 3));
    default:
        throw new Error(`Unknown period: ${period}`);
    }
}


function determineActiveRange() {
    const start = new Date(startDate.value);
    const end = new Date(endDate.value);
    const todayDate = new Date(today);

    const monthDiff = (end.getFullYear() - start.getFullYear()) * 12 + end.getMonth() - start.getMonth();
    const dayDiff = end.getDate() - start.getDate();

    if (formatDate(start) === formatDate(todayDate) && formatDate(end) === formatDate(todayDate)) {
        activeRange.value = "today";
    } else if (Math.round((end - start) / (1000 * 60 * 60 * 24)) <= 5 && formatDate(end) === formatDate(todayDate)) {
        activeRange.value = "5D";
    } else if (monthDiff === 1 && dayDiff === 0) {
        activeRange.value = "1M";
    } else if (monthDiff === 3 && dayDiff === 0) {
        activeRange.value = "3M";
    } else {
        activeRange.value = "";
    }
}

watch([startDate, endDate], () => {
    determineActiveRange();
}, { immediate: true });
</script>

<style scoped>
.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.period-buttons {
  display: flex;
  gap: 10px;
}

.date-picker {
  display: flex;
  justify-content: space-between;
}

.input-container {
  border: 1px solid #cccccc;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  padding: 5px;
  margin: 5px;
  min-width: 180px;
  background-color: #f1f2f3;
}

.date-label {
  font-size: 10px;
  color: #333333;
}

.date-input {
  border: none;
  font-size: 16px;
  background-color: #f1f2f3;
  cursor: pointer;
}

.date-input:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.5);
}

@media (max-width: 768px) {
  .container {
    display: flex;
    flex-direction: column;
  }

  .date-picker {
    flex-direction: column;
  }

  .input-container {
    width: 100%;
  }
}
</style>
