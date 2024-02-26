<template>
  <base-card>
    <div class='container'>
      <h1><a target='_blank' href="https://www.set.or.th/en/home">SET</a> News Analysis Bot</h1>
      <p>Gathers
        <a href="https://www.set.or.th/en/market/news-and-alert/news?source=company&securityType=S&keyword=F45"
          target="_blank">Financial Performance Yearly (F45) Reports</a>
        from the Stock Exchange of Thailand and extracts
        <a href="https://www.investopedia.com/terms/e/eps.asp" target="_blank">Earnings Per Share (EPS)</a>
        data.
      </p>
    </div>
  </base-card>
</template>


<style scoped>
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.container h1 {
  font-size: 50px;
  margin: 0;
  text-align: center;
}

.container p {
  text-align: center;
}
</style>
