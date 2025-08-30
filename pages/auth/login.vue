<script setup lang="ts">
import axios from "axios";
import { ref } from "vue";

const email = ref<string>("");
const pass = ref<string>("");
const code = ref<string>("");
const errorMessage = ref<string>("");
const recovery = ref<boolean>(false);
const checkRecovery = ref<boolean>(false);

const config = useRuntimeConfig();
const apiBase = config.public.apiBase;
const errorMsg = ref<string>("");
const userInfo = useAuthStore();

const goHome = () => {
  navigateTo("/");
};

const validateForm = (): boolean => {
  if (!email.value.trim()) {
    errorMessage.value = "Поле 'почта' не может быть пустым.";
    return false;
  }

  if (!pass.value.trim()) {
    errorMessage.value = "Поле 'пароль' не может быть пустым.";
    return false;
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email.value)) {
    errorMessage.value = "Введите корректный адрес электронной почты.";
    return false;
  }

  if (pass.value.length < 6) {
    errorMessage.value = "Пароль должен содержать минимум 6 символов.";
    return false;
  }

  errorMessage.value = "";
  return true;
};

const login = async () => {
  try {
    if (!validateForm()) {
      return;
    }

    const formData = {
      email: email.value,
      password: pass.value,
    };

    const response = await axios.post(`${apiBase}/api/auth/login/`, formData);
    const authToken = useCookie("auth_token", {
      httpOnly: false,
      secure: true,
      sameSite: "strict",
      maxAge: 300,
    });
    const refreshToken = useCookie("refresh_token", {
      httpOnly: false,
      secure: true,
      sameSite: "strict",
      maxAge: 86400,
    });
    const userEmail = useCookie("userEmail", {
      httpOnly: false,
      secure: true,
      sameSite: "strict",
      maxAge: 86400,
    });

    authToken.value = response.data.tokens.access;
    refreshToken.value = response.data.tokens.refresh;
    userEmail.value = email.value;
    userInfo.loginUser();
  } catch (error: any) {
    if (error.response) {
      errorMessage.value = "Что-то не совпадает, проверьте свои данные";
    } else {
      console.error(error);
      alert("Произошла ошибка при отправке запроса.");
    }
  }
};

const passRecoveryGet = async () => {
  try {
    const response = await axios.get(`${apiBase}/api/passRecovery/`, {
      params: {
        email: email.value,
      },
    });

    if (response.status == 200) {
      checkRecovery.value = true;
      recovery.value = false;
    }
  } catch (error: any) {
    console.error(error);
    if (error.status == 400) {
      errorMsg.value = "Данная почта не найдена";
    } else if (error.status == 429) {
      errorMsg.value = "Частые запросы, подождите 2 минуты";
    } else {
      alert("Произошла ошибка при отправке запроса.");
    }
  }
};

const passRecoveryPost = async () => {
  try {
    const formData = {
      email: email.value,
      code: code.value,
      pass: pass.value,
    };

    const response = await axios.post(`${apiBase}/api/passRecovery/`, formData);

    if (response.status == 200) {
      checkRecovery.value = false;
    }
  } catch (error: any) {
    if (error.status == 400) {
      alert("Что-то введено не верно");
    } else if (error.status == 403) {
      alert("Время действия кода истекло");
      checkRecovery.value = false;
      recovery.value = true;
    } else {
      alert("Произошла ошибка при отправке запроса.");
    }
  }
};
</script>

<template>
  <div class="HelloText">
    <h1 class="flex justify-center">
      Приветствуем вас на
      <p>Барахолке</p>
    </h1>
    <h1>
      Здесь можно покупать и продавать свои вещи, предлагать услуги и искать
      попутчиков.
    </h1>
    <h1>
      Просим соблюдать
      <a class="rules-link" href="/rules">правила</a> площадки и быть вежливым в
      чатах!
    </h1>
  </div>
  <div class="log-form shadow-md">
    <div class="logo" @click="goHome()">
      <img
        class="h-24 self-center"
        src="../../assets/image/logo.png"
        alt="Logo"
      />
    </div>
    <form
      v-if="!recovery && !checkRecovery"
      @submit.prevent="login"
      class="login-form"
    >
      <input
        type="email"
        placeholder="почта"
        v-model="email"
        class="input"
        required
      />
      <input
        type="password"
        placeholder="пароль"
        v-model="pass"
        class="input"
        required
      />
      <div v-if="errorMessage" class="error-message text-red-500 text-sm">
        {{ errorMessage }}
      </div>
      <div class="flex justify-between">
        <button type="submit" class="btn log">вход</button>
        <a class="btn" href="/auth/register">регистрация</a>
      </div>
      <a @click="recovery = true" class="recoveryLink">забыли пароль?</a>
    </form>
    <form
      v-if="recovery"
      @submit.prevent="passRecoveryGet"
      class="recoveryPass"
    >
      <h1>{{ errorMsg }}</h1>
      <input
        type="email"
        placeholder="почта"
        v-model="email"
        class="input"
        required
      />
      <button type="submit" class="btn">отправить</button>
    </form>
    <form
      v-if="checkRecovery"
      @submit.prevent="passRecoveryPost"
      class="recoveryPass"
    >
      <input
        type="email"
        placeholder="почта"
        v-model="email"
        class="input"
        required
      />
      <div>На данную почту был отправлен код для востановления пароля</div>
      <input
        type="text"
        placeholder="Введите код c почты"
        v-model="code"
        class="input"
        required
      />
      <input
        type="text"
        placeholder="Введите новый пароль"
        v-model="pass"
        class="input"
        required
      />
      <button type="submit" class="btn">изменить</button>
    </form>
  </div>
</template>

<style lang="scss" scoped>
@use "~/assets/scss/main.scss" as main;
@use "sass:color";

.content {
  height: max-content + 10px;
}

.recoveryPass {
  width: 70%;
  display: flex;
  flex-direction: column;
  height: auto;

  div {
    margin: 0;
    font-size: 12px;
    margin-left: 10px;
  }

  h1 {
    font-weight: 18px;
  }

  .input,
  button {
    width: 100% !important;
    margin-bottom: 5px;
  }
}

.rules-link {
  margin-left: 10px;
  margin-right: 10px;

  &:hover {
    opacity: 80%;
    text-decoration: underline;
    cursor: pointer;
  }
}
.recoveryLink {
  margin-left: auto;
  margin-right: auto;
  cursor: pointer;

  &:hover {
    border-bottom: 1px solid black;
    color: blue;
  }
}
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

.login-form {
  @apply flex flex-col space-y-1 self-center;
  width: 70%;
}

input {
  border: 2px solid main.$second-color;
  font-size: 20px;

  &::placeholder {
    color: main.$second-color;
    font-weight: 600;
  }

  &:focus {
    border-color: color.adjust(main.$second-color, $lightness: -10%);
  }
}

.btn {
  width: 65%;
  font-weight: 600;
  text-align: center;
  align-items: center;
  font-size: 20px;
}

.log {
  background-color: main.$second-color;
  width: 30%;

  &:hover {
    background-color: color.adjust(main.$second-color, $lightness: -5%);
  }
}

.log-form {
  @apply flex items-center;
  background-color: color.scale(
    main.$window-color,
    $lightness: +15%,
    $alpha: -10%
  );
  width: 70%;
  margin: auto;
  position: relative;
  top: calc(100vh / 4);
  border-radius: 10px;
  height: 180px;
}

.error-message {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: red;
}

@media (min-width: 1600px) {
  .log-form {
    width: 50%;
  }
}

@media (max-width: 1024px) {
  .log-form {
    display: block;
    width: 600px;
    height: 450px;
    top: 5vh;
    padding: 50px;
    margin-bottom: 100px;

    * {
      margin-left: auto;
      margin-right: auto;
    }

    input,
    .login-form {
      width: 480px;
      font-size: 16px;
      height: 50px;
    }

    .btn {
      width: 230px;
      margin: 0;
      font-size: 16px;
      height: 50px;
      text-align: center;
      align-items: center;
      display: flex;
      justify-content: center;
    }

    div:has(.btn) {
      margin: 0;
    }
  }
}

@media (max-width: 680px) {
  .HelloText {
    font-size: 24px;
    line-height: 25px;
    font-weight: bolder;
  }

  .log-form {
    width: 480px;
    top: 2vh;
    padding: 20px;

    * {
      margin-left: auto;
      margin-right: auto;
    }

    .login-form {
      width: 420px;
      height: max-content;

      input {
        width: 420px;
        font-size: 16px;
        height: 40px;
      }
    }

    .btn {
      width: 420px;
      margin: 5px 0 0 0;
      font-size: 16px;
      height: 40px;
    }

    div:has(.btn) {
      margin: 0;
      display: block;
    }
  }
}

@media (max-width: 560px) {
  .HelloText {
    font-size: 20px;
    line-height: 25px;
    font-weight: bolder;
  }
}

@media (max-width: 500px) {
  .HelloText {
    font-size: 4vw;
    line-height: 20px;
    font-weight: bolder;
    margin: 0;
    padding-left: 0;
    padding-right: 0;
  }

  .log-form,
  .btn,
  .login-form,
  input {
    width: 100% !important;
  }
}
</style>
