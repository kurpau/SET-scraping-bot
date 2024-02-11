<template>
  <tr>
    <td data-label="Name"> {{ stock.name }}</td>
    <td data-label="Tikcer">{{ stock.symbol }}</td>
    <td data-label="EPScurr">{{ stock.eps[0] }}</td>
    <td data-label="EPSprev">{{ stock.eps[1] }}</td>
  </tr>
</template>

<script setup>
defineProps(["stock"]);
</script>

<style scoped>
td {
  text-align: center;
}
</style>
