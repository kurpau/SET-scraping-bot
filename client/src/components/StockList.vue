<template>
  <table>
    <thead>
      <tr>
        <th scope="col">TICKER</th>
        <th scope="col">EPS</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="stock in stocks" :key="stock.id">
        <td>{{ stock.symbol }}</td>
        <td>{{ stock.eps }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
// import StockItem from "./StockItem.vue";

defineProps(["stocks"]);
</script>
