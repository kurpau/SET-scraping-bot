<template>
  <RouterView />
</template>

<script setup>
import { RouterView } from "vue-router";
</script>

<style>
:root {
  --color-background: #fafbfc;
  --color-background-hover: #f3f4f6;
  --color-background-selected: #edeff2;
  --color-text: #24292e;
  --color-text-disabled: #959da5;
  --color-border: rgba(27, 31, 35, 0.15);
  --color-fg-muted: #656d76;
  --color-accent-fg: #0969da;
  --card-shadow: rgba(0, 0, 0, 0.25);
}

* {
  box-sizing: border-box;
}

html {
  font-family: -apple-system, system-ui, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji"
}

body {
  margin: 0;
}

a {
  color: var(--color-fg-muted);
  text-decoration: none;
}

a:hover {
  cursor: pointer;
  color: var(--color-accent-fg);
}
</style>
