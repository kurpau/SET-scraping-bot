<template>
  <base-card>
    <div class="container">
      <date-picker @update-dates="handleDateUpdate"></date-picker>
      <div class='fetch'>
        <base-button id="fetch-button" @click="fetchStocks">Fetch Stocks</base-button>
      </div>
    </div>
  </base-card>
</template>

<script setup>
import DatePicker from "./DatePicker.vue";

import { ref, watch } from "vue";
import { useRouter } from "vue-router";

const emit = defineEmits(["fetchStocks", "updateLoading"]);
const isLoading = ref(false);
const router = useRouter();
const startDate = ref("");
const endDate = ref("");

function handleDateUpdate({ start, end }) {
  startDate.value = start;
  endDate.value = end;
  router.push({ path: "/", query: { fromDate: start, toDate: end } });
}

async function fetchStocks() {
  if (isLoading.value) {
    console.log("Request is already in progress.");
    return;
  }

  isLoading.value = true;

  try {
    const path = `http://localhost:5000/stocks?from=${startDate.value}&to=${endDate.value}`;
    const res = await fetch(path);
    const data = await res.json();

    emit("fetchStocks", [...data.stocks]);
    localStorage.setItem("stocksData", JSON.stringify(data.stocks));
  } catch (error) {
    console.error("Something went wrong!", error);
    localStorage.removeItem("stocksData");
  } finally {
    isLoading.value = false;
  }
}

watch(isLoading, (newLoadingState) => {
  emit("updateLoading", newLoadingState);
});
</script>

<style scoped>
#fetch-button {
  display: inline-block;
}

.fetch {
  display: flex;
  gap: 10px;
  margin-left: auto;
  margin-right: 0;
  justify-content: flex-end;
  align-items: center;
}
</style>
