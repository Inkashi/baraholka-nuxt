<script setup lang="ts">
import axios from "axios";

const email = ref<string>("");
const name = ref<string>("");
const pass = ref<string>("");
const verifypass = ref<string>("");

const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

const submitForm = async () => {
  try {
    const formData = {
      name: name.value,
      email: email.value,
      password: pass.value,
    };

    const response = await axios.post(
      `${apiBase}/api/auth/register/`,
      formData
    );
    console.log(response.data);
    alert(response.data || "Вы успешно зарегистрированы!");
  } catch (error: any) {
    if (error.response) {
      console.error(error.response.data);
      alert(
        "Ошибка регистрации: " + error.response.data.detail ||
          "Что-то пошло не так"
      );
    } else {
      console.error(error);
      alert("Произошла ошибка при отправке запроса.");
    }
  }
};
</script>
<template>
  <a class="arrow-back" href="/auth/login">Вернуться</a>
  <div class="h-screen flex items-center justify-center">
    <div class="reg-card">
      <div class="logo">
        <img
          class="h-24 self-center"
          src="../../assets/image/logo.png"
          alt="Logo"
        />
      </div>
      <div class="flex items-center mr-35 self-center">
        <form @submit.prevent="submitForm" class="flex flex-col w-96">
          <input
            type="email"
            placeholder="почта"
            v-model="email"
            class="input"
          />
          <input type="text" placeholder="имя" v-model="name" class="input" />
          <input
            type="password"
            placeholder="пароль"
            v-model="pass"
            class="input"
          />
          <input
            type="password"
            placeholder="повторите пароль"
            v-model="verifypass"
            class="input"
          />
          <p class="text-center">
            Нажимая кнопку регистрации вы соглашаетесь с
            <a class="link" href="#">пользовотельским соглашением</a>
          </p>
          <button class="btn" type="submit">Зарегистрироваться</button>
        </form>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "~/assets/scss/main.scss" as main;
@use "sass:color";
.arrow-back {
  margin: 50px;
  margin-top: 20px;
  position: absolute;
  width: 60px;
  height: 60px;
  border-bottom: 10px solid main.$primary-color;
  border-left: 10px solid main.$second-color;
  transform: rotate(90deg);
  transition: 0.5s;
  color: transparent;
  font-weight: bold;

  &:hover {
    transform: rotate(45deg);
    color: main.$primary-color;
  }
}

.link {
  @apply underline decoration-transparent transition duration-300 ease-in-out hover:decoration-inherit;
  color: rgb(0, 81, 255);
}

p {
  color: main.$primary-color;
}

.reg-card {
  @apply w-max flex justify-center flex-col shadow-md;
  background-color: color.scale(
    main.$window-color,
    $lightness: +15%,
    $alpha: -10%
  );
  padding: 1rem 8rem;
  border-radius: 10px;
}

.logo {
  @apply mb-2 self-center shadow-md rounded-full h-32 w-32 flex justify-center;
  background-color: color.adjust(main.$window-color, $lightness: +5%);
}

.btn {
  @apply shadow-md mt-3 place-self-center;
  font-size: 18px !important;
}
</style>
