<template>
  <table>
    <thead>
      <tr>
        <th>TICKER</th>
        <th>EPS</th>
        <th>FULL NAME</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="stock in stocks" :key="stock.id">
        <td>{{ stock.symbol }}</td>
        <td>{{ stock.eps }}</td>
        <td>{{ stock.name }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
// import StockItem from "./StockItem.vue";

defineProps(["stocks"]);
</script>
