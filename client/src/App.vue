<template>
  <RouterView />
</template>

<script setup>
import { RouterView } from "vue-router";
</script>

<style>
:root {
  --color100: #f0f6fc;
  --color200: #c9d1d9;
  --color300: #b1bac4;
  --color400: #8b949e;
  --color500: #6e7681;
  --color600: #484f58;
  --color700: #30363d;
  --color800: #21262d;
  --color900: #161b22;
  --color1000: #0d1117;
}

* {
  box-sizing: border-box;
}

html {
  font-family: "Roboto", sans-serif;
}

body {
  margin: 0;
}
</style>
