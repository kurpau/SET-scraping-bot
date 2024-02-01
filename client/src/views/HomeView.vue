<template>
  <header-panel></header-panel>
  <stock-list :stocks="stocks"></stock-list>
</template>

<script setup>
import HeaderPanel from "../components/HeaderPanel.vue";
import StockList from "../components/StockList.vue";
</script>
