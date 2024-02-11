<template>
  <base-card>
    <div class='info' v-if="isLoading">
      <base-spinner></base-spinner>
    </div>
    <div v-else>
      <table v-if="stocks">
        <caption>Fetch Results</caption>
        <thead>
          <tr>
            <th scope="col">Name</th>
            <th scope="col">Ticker</th>
            <th scope="col">EPS curr</th>
            <th scope="col">EPS prev</th>
          </tr>
        </thead>
        <tbody>
          <stock-item v-for="stock in stocks" :key="stock.id" :stock="stock"></stock-item>
        </tbody>
      </table>
      <div class="info" v-else>
        <p>Select a date range and click 'Fetch Stocks' to see the latest stock information.</p>
      </div>
    </div>
  </base-card>
</template>

<script setup>
import StockItem from "./StockItem.vue";
defineProps(["stocks", "isLoading"]);
</script>

<style scoped>
.info {
  display: flex;
  justify-content: center;
  align-items: center;
}


table {
  border: 1px solid #ccc;
  border-collapse: collapse;
  margin: 0;
  padding: 0;
  width: 100%;
  table-layout: fixed;
}

table caption {
  font-size: 1.5em;
  margin: .5em 0 .75em;
}

table tr {
  background-color: #f8f8f8;
  border: 1px solid #ddd;
  padding: .35em;
}

table th,
table td {
  padding: .625em;
  text-align: center;
}

table th {
  font-size: .85em;
  letter-spacing: .1em;
  text-transform: uppercase;
}

@media screen and (max-width: 600px) {
  table {
    border: 0;
  }

  table caption {
    font-size: 1.3em;
  }

  table thead {
    border: none;
    clip: rect(0 0 0 0);
    height: 1px;
    margin: -1px;
    overflow: hidden;
    padding: 0;
    position: absolute;
    width: 1px;
  }

  table tr {
    border-bottom: 3px solid #ddd;
    display: block;
    margin-bottom: .625em;
  }

  table td {
    border-bottom: 1px solid #ddd;
    display: block;
    font-size: .8em;
    text-align: right;
  }

  table td::before {
    /*
    * aria-label has no advantage, it won't be read inside a table
    content: attr(aria-label);
    */
    content: attr(data-label);
    float: left;
    font-weight: bold;
    text-transform: uppercase;
  }

  table td:last-child {
    border-bottom: 0;
  }
}
</style>
