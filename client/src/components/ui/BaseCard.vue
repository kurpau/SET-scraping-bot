<template>
  <div class="card">
    <slot></slot>
  </div>
</template>

<style scoped>
.card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  padding: 1rem;
  margin: 2rem auto;
  max-width: 40rem;
}

@media (max-width: 880px) {
  .card {
    margin: 1rem auto;
  }
}

/* Responsive adjustments */
@media (max-width: 670px) {
  .card {
    margin: 1rem auto;
    max-width: 30rem;
  }
}
</style>
