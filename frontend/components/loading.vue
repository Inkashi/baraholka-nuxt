<template>
  <div class="loading">
    <div class="spinner"></div>
    <p>Загрузка...</p>
  </div>
</template>

<script setup lang="ts"></script>

<style lang="scss" scoped>
@use "~/assets/scss/main.scss" as main;
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh;

  .spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-left-color: main.$primary-color;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
  }

  p {
    margin-top: 10px;
    font-size: 18px;
    color: main.$second-color;
    font-weight: bold;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
