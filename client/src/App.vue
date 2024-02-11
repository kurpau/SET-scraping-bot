<template>
  <RouterView />
</template>

<script setup>
import { RouterView } from "vue-router";
</script>

<style>
:root {
  --seasalt: #f8f9faff;
  --antiflash-white: #e9ecefff;
  --platinum: #dee2e6ff;
  --french-gray: #ced4daff;
  --french-gray-2: #adb5bdff;
  --slate-gray: #6c757dff;
  --outer-space: #495057ff;
  --onyx: #343a40ff;
  --eerie-black: #212529ff;
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
