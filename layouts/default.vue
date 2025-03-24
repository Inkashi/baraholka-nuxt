<template>
  <div class="background"></div>
  <div class="page-container">
    <div class="block">
      <header class="header bg-[#00569d]">
        <div
          class="mx-auto ml-10 mr-20 mb-10 px-2 py-2 flex justify-between items-center"
          v-if="!isAuthRoute"
        >
          <div class="logo relative">
            <div class="bg-[#00569d] rounded-full size-28 absolute home">
              <a
                href="/"
                class="z-10 bg-white rounded-full size-20 flex justify-center items-center"
              >
                <img
                  src="/assets/image/logo.png"
                  alt="Logo"
                  class="h-12 z-10"
                />
              </a>
            </div>
          </div>
          <nav class="gap-4 z-10">
            <div v-if="isAuth" class="flex items-center">
              <a href="/chats"
                ><Icon v-if="!hasUnreadMessages"
                  name="tabler:message-circle-filled"
                  size="48"
                  color="blue"
              />
              <Icon v-if="hasUnreadMessages"
                  name="tabler:message-circle-exclamation "
                  size="48"
                  color="blue"
              /></a>
              <a
                href="/createProduct"
                class="bg-white hover:bg-white-500 text-white font-semibold py-2 px-4 rounded-full flex items-center h-10"
              >
                <i class="fas fa-comment-alt mr-2"></i>
                <p class="text-blue-600">Разместить объявление</p>
              </a>
              <a href="/account"
                ><Icon name="ic:round-account-circle" size="48"
              /></a>
              <a href="/favorites"><Icon name="mdi:heart" size="48" /></a>
            </div>
            <div v-else>
              <a
                href="/auth/login"
                class="bg-white hover:bg-white-500 text-white font-semibold py-2 px-4 rounded-full flex items-center h-10"
              >
                <i class="fas fa-comment-alt mr-2"></i>
                <p class="text-blue-600">Войти</p>
              </a>
            </div>
          </nav>
        </div>
      </header>
    </div>
    <main class="content">
      <slot></slot>
    </main>

    <footer
      class="footer bg-[#00569d] w-full text-white flex items-center justify-center flex-col"
    >
      <div class="max-w-max text-center mb-3 mt-3">
        <div class="space-y-1 mb-3">
          <p>Контактные данные:</p>
          <p>Телефон: <a href="tel:78005553535">+7 800 555 35 35</a></p>
          <p>Почта: <a href="mailto:baraholka@ugra.su">baraholka@ugra.su</a></p>
        </div>
        <div>
          <p>Адрес: г.Ханты-Мансийск, ул.Чехова д.16</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

const route = useRoute();
const userStore = useAuthStore();

const config = useRuntimeConfig();
const apiBase = config.public.apiBase as string;

const isAuth = ref(userStore.isAuth);

const userId = ref();
const hasUnreadMessages = ref(false);

watch(
  () => userStore.isAuth,
  (newIsAuth) => {
    isAuth.value = newIsAuth;
  }
);

const isAuthRoute = computed(() => {
  return route.name === "auth-register" || route.name === "auth-login";
});

const fetchUserData = async () => {
  try {
    const token = useCookie<string | null>("auth_token").value;
    const decodedToken: any = jwtDecode(token!);

    userId.value = decodedToken.user_id || null;

    checkUnreadMessages();

  }
  catch (e) {
    console.log(e)
  }
};

const checkUnreadMessages = async () => {
  try {
    const response = await axios.get(`${apiBase}/api/UnreadMessagesCheck/`, {
      params: {id:userId.value}
    });
    hasUnreadMessages.value = response.data.has_unread_messages;
  } catch (error) {
    console.error("Ошибка при проверке непрочитанных сообщений:", error);
  }
};

onMounted(() => {
  fetchUserData();
});

</script>

<style lang="scss">
@use "~/assets/scss/main.scss" as main;

.page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: rgba(main.$window-color, 0.7);
}

.header {
  position: relative;

  a:hover {
    opacity: 0.8;
    transform: scale(0.95);
    transition: all 1s;
  }

  a {
    transition: all 1s;
  }
  .iconify {
    color: white;
  }

  .logo {
    @apply flex justify-center items-center;
  }
}

.home {
  @apply absolute rounded-full size-28 z-10 absolute flex justify-center items-center;
  margin-top: 2rem;
  left: 5%;
}

.home:hover {
  transform: rotate(-360deg) !important;
  transition: all 1s;
}

.content {
  flex: 1;
  padding: 0 20px;
}

.footer {
  margin-top: 5%;

  a:hover {
    color: rgb(140, 199, 255);
    text-decoration: underline;
  }
}
</style>
