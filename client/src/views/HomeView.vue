<template>
  <project-card />
  <header-panel @updateLoading="setLoadingState" @fetchStocks="updateStocks"></header-panel>
  <stock-list :isLoading="isLoading" :fetchedStocks="stocks"></stock-list>
</template>

<script setup>
import { ref } from "vue";
import HeaderPanel from "../components/HeaderPanel.vue";
import StockList from "../components/StockList.vue";
import ProjectCard from "../components/ProjectCard.vue";

const stocks = ref();

const isLoading = ref(false);

function setLoadingState(newState) {
  isLoading.value = newState;
}

function updateStocks(e) {
  stocks.value = e;
}
</script>
