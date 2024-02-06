<template>
  <header-panel @fetchStocks="updateStocks"></header-panel>
  <stock-list :stocks="stocks"></stock-list>
</template>

<script setup>
import { ref } from "vue";
import HeaderPanel from "../components/HeaderPanel.vue";
import StockList from "../components/StockList.vue";

let stocks = ref();
function updateStocks(event) {
  stocks.value = event;
}
</script>
