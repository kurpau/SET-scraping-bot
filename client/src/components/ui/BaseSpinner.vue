<template>
  <div class="lds-facebook">
    <div></div>
    <div></div>
    <div></div>
  </div>
</template>

<style scoped>
.lds-facebook {
  display: inline-block;
  position: relative;
  width: 34px;
  height: 34px;
}

.lds-facebook div {
  display: inline-block;
  position: absolute;
  left: 2px;
  width: 6px;
  background: #000;
  animation: lds-facebook 1.2s cubic-bezier(0, 0.5, 0.5, 1) infinite;
}

.lds-facebook div:nth-child(1) {
  left: 2px;
  animation-delay: -0.24s;
}

.lds-facebook div:nth-child(2) {
  left: 14px;
  animation-delay: -0.12s;
}

.lds-facebook div:nth-child(3) {
  left: 26px;
  animation-delay: 0;
}

@keyframes lds-facebook {
  0% {
    top: 2px;
    height: 30px;
  }

  50%,
  100% {
    top: 10px;
    height: 14px;
  }
}
</style>
