<script setup lang="ts">
const email = ref<string>("");
const pass = ref<string>("");

const login = () => {
  console.log(email);
};
</script>

<template>
  <div class="HelloText">
    <h1 class="flex justify-center">
      Приветствуем вас на
      <p>Барахолке ЮГУ</p>
    </h1>
    <h1>
      Здесь студенты могут покупать и продавать свои вещи, предлагать услуги и
      искать попутчиков.
    </h1>
    <h1>Просим соблюдать правила площадки и быть вежливым в чатах!</h1>
  </div>
  <div class="log-form shadow-md">
    <div class="logo">
      <img
        class="h-24 self-center"
        src="../../assets/image/logo.png"
        alt="Logo"
      />
    </div>
    <form
      @submit.prevent="login"
      class="flex flex-col w-96 space-y-1 self-center"
    >
      <input type="email" placeholder="почта" v-model="email" class="input" />
      <input
        type="password"
        placeholder="пароль"
        v-model="pass"
        class="input"
      />
      <div class="flex space-x-4">
        <button type="submit" class="btn log">вход</button>
        <a class="btn" href="/auth/register">регистрация</a>
      </div>
    </form>
  </div>
</template>

<style lang="scss" scoped>
@use "~/assets/scss/main.scss" as main;
@use "sass:color";
h1 {
  text-align: center;
  color: main.$second-color;
  display: flex;
  justify-content: center;
  width: 100%;
}

p {
  margin-left: 1rem;
  color: main.$primary-color;
  font-weight: bold;
}

.HelloText {
  font-size: 2rem;
  line-height: 2rem;
  font-weight: 600;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 1rem 4rem;
}

input {
  border: 2px solid main.$second-color;
  &::placeholder {
    color: main.$second-color;
    font-weight: 600;
  }

  &:focus {
    border-color: color.adjust(main.$second-color, $lightness: -10%);
  }
}

.log {
  background-color: main.$second-color;
  width: 30% !important;

  &:hover {
    background-color: color.adjust(main.$second-color, $lightness: -5%);
  }
}

.btn {
  width: 70%;
  font-weight: 600;
  text-align: center;
  align-items: center;
  font-size: 1vw;
}

.log-form {
  @apply flex items-center;
  background-color: color.scale(
    main.$window-color,
    $lightness: +15%,
    $alpha: -10%
  );
  width: max-content;
  margin: auto;
  position: relative;
  top: calc(100vh / 4);
  border-radius: 10px;
  width: 45rem;
  height: 10rem;
}

.logo {
  @apply mb-2 mr-2 shadow-md rounded-full h-32 w-32 flex justify-center;
  background-color: color.adjust(main.$window-color, $lightness: +5%);
  margin-left: 5%;
  margin-right: 5%;
}
</style>
