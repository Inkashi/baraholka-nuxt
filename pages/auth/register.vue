<script setup lang="ts">
import axios from "axios";

const email = ref<string>("");
const name = ref<string>("");
const pass = ref<string>("");
const verifypass = ref<string>("");

const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

const errors = ref<{ [key: string]: string }>({});

const validateForm = (): boolean => {
  errors.value = {};

  if (!email.value) {
    errors.value.email = "Почта обязательна.";
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    errors.value.email = "Введите корректный email.";
  }

  if (!name.value) {
    errors.value.name = "Имя обязательно.";
  } else if (name.value.length < 3) {
    errors.value.name = "Имя должно содержать минимум 3 символа.";
  }

  if (!pass.value) {
    errors.value.password = "Пароль обязателен.";
  } else if (pass.value.length < 6) {
    errors.value.password = "Пароль должен содержать минимум 6 символов.";
  }

  if (!verifypass.value) {
    errors.value.verifypass = "Подтвердите пароль.";
  } else if (pass.value !== verifypass.value) {
    errors.value.verifypass = "Пароли не совпадают.";
  }

  return Object.keys(errors.value).length === 0;
};

const submitForm = async () => {
  if (!validateForm()) {
    return;
  }

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
  <div class="reg-form">
    <div class="reg-card">
      <div class="logo">
        <img
          class="size-15 self-center"
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
          <p v-if="errors.email" class="text-red-500 text-sm">
            {{ errors.email }}
          </p>

          <input type="text" placeholder="имя" v-model="name" class="input" />
          <p v-if="errors.name" class="text-red-500 text-sm">
            {{ errors.name }}
          </p>

          <input
            type="password"
            placeholder="пароль"
            v-model="pass"
            class="input"
          />
          <p v-if="errors.password" class="text-red-500 text-sm">
            {{ errors.password }}
          </p>

          <input
            type="password"
            placeholder="повторите пароль"
            v-model="verifypass"
            class="input"
          />
          <p v-if="errors.verifypass" class="text-red-500 text-sm">
            {{ errors.verifypass }}
          </p>

          <p class="text-center">
            Нажимая кнопку регистрации вы соглашаетесь с
            <a class="link" href="#">пользовательским соглашением</a>
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

.reg-form {
  @apply h-screen flex items-center justify-center;
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
  padding: 3%;
}

.btn {
  @apply shadow-md mt-3 place-self-center;
  font-size: 18px !important;
}
</style>
