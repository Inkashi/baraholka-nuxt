<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

const route = useRoute();
const router = useRouter();

const userStore = useAuthStore();
const config = useRuntimeConfig();
const apiBase = config.public.apiBase;
const mobileMenuOpen = ref(false);
const isAuth = ref(userStore.isAuth);
const hasUnreadMessages = ref(false);
const userId = ref<string | null>(null);
const userEmail = ref();
const showModal = ref(false);
const msg = ref();
const isAuthRoute = computed(() => {
  return route.name === "auth-register" || route.name === "auth-login";
});

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value;
  document.body.style.overflow = mobileMenuOpen.value ? "hidden" : "";
};

const closeMobileMenu = () => {
  mobileMenuOpen.value = false;
  document.body.style.overflow = "";
};

const fetchUserData = async () => {
  try {
    const token = useCookie<string | null>("auth_token").value;
    if (token) {
      const decodedToken: any = jwtDecode(token);
      userId.value = decodedToken.user_id || null;
      await checkUnreadMessages();
    }
  } catch (error) {
    console.error("Ошибка при получении данных пользователя:", error);
  }
};

const checkUnreadMessages = async () => {
  try {
    const response = await axios.get(`${apiBase}/api/UnreadMessagesCheck/`, {
      params: { id: userId.value },
    });
    hasUnreadMessages.value = response.data.has_unread_messages;
  } catch (error) {
    console.error("Ошибка при проверке непрочитанных сообщений:", error);
  }
};

const sendMsg = async () => {
  if (!msg) {
    console.log("Поле пустое");
    return;
  }

  const formData = new FormData();
  formData.append("email", userEmail.value);
  formData.append("msg", msg.value);
  try {
    const response = await axios.post(`${apiBase}/api/feedback/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    if (response.status === 200) {
      showModal.value = false;
      msg.value = "";
    }
  } catch (error) {
    console.error("Ошибка при создании товара:", error);
    alert("Произошла ошибка при создании товара.");
  }
};

const getSupport = () => {
  console.log("Я тут");
  userEmail.value = useCookie<string | null>("userEmail").value;
  showModal.value = true;
  closeMobileMenu;
};

watch(
  () => route.path,
  () => {
    if (mobileMenuOpen.value) closeMobileMenu();
  }
);

watch(
  () => userStore.isAuth,
  (newAuthState) => {
    isAuth.value = newAuthState;
    if (!newAuthState && mobileMenuOpen.value) closeMobileMenu();
  }
);

onMounted(async () => {
  if (isAuth.value) {
    await fetchUserData();
  }
});
</script>

<template>
  <div class="background"></div>
  <div class="page-container">
    <div class="block">
      <header class="header bg-[#00569d]">
        <div class="head-links" v-if="!isAuthRoute">
          <div class="logo-df relative">
            <div class="bg-[#00569d] rounded-full size-28 absolute home">
              <a
                href="/"
                class="z-10 bg-white rounded-full size-20 flex justify-center items-center"
              >
                <img
                  src="/assets/image/logo.png"
                  alt="logo-df"
                  class="h-12 z-10"
                />
              </a>
            </div>
          </div>

          <button
            v-if="isAuth"
            @click="toggleMobileMenu"
            class="mobile-menu-button lg:hidden z-20"
            aria-label="Открыть меню"
          >
            <Icon name="ic:round-menu" size="32" color="white" />
          </button>
          <nav v-if="isAuth" class="gap-4 z-10 hidden lg:flex">
            <div class="flex items-center">
              <a href="/chats">
                <Icon
                  v-if="!hasUnreadMessages"
                  name="tabler:message-circle-filled"
                  size="48"
                  color="blue"
                />
                <Icon
                  v-if="hasUnreadMessages"
                  name="tabler:message-circle-exclamation"
                  size="48"
                  color="blue"
                />
              </a>
              <a
                href="/createProduct"
                class="bg-white hover:bg-white-500 text-white font-semibold py-2 px-4 rounded-full flex items-center h-10"
              >
                <i class="fas fa-comment-alt mr-2"></i>
                <p class="text-blue-600">Разместить объявление</p>
              </a>
              <a href="/account">
                <Icon name="ic:round-account-circle" size="48" />
              </a>
              <a href="/favorites">
                <Icon name="mdi:heart" size="48" />
              </a>
              <button @click="getSupport">
                <Icon name="material-symbols:contact-support" size="48"></Icon>
              </button>
            </div>
          </nav>
          <nav v-else>
            <div>
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

        <div v-if="isAuth" class="lg:hidden">
          <div
            class="fixed inset-0 bg-[#00569d] z-50 transform -translate-x-full transition-transform duration-300"
            :class="{ 'translate-x-0': mobileMenuOpen }"
            @click.self="closeMobileMenu"
          >
            <div
              class="p-6 h-full w-full flex flex-col items-center justify-start"
            >
              <button
                @click="closeMobileMenu"
                class="absolute top-4 right-4 z-50"
                aria-label="Закрыть меню"
              >
                <Icon name="ic:round-close" size="32" color="white" />
              </button>

              <nav class="flex flex-col items-center gap-8 mt-16 w-full">
                <a
                  href="/account"
                  @click="closeMobileMenu"
                  class="w-full text-center text-white"
                >
                  <div class="flex items-center justify-center gap-2">
                    <Icon name="ic:round-account-circle" size="32" />
                    <span>Профиль</span>
                  </div>
                </a>

                <a
                  href="/chats"
                  @click="closeMobileMenu"
                  class="w-full text-center text-white"
                >
                  <div class="flex items-center justify-center gap-2">
                    <Icon
                      v-if="!hasUnreadMessages"
                      name="tabler:message-circle-filled"
                      size="32"
                      color="blue"
                    />
                    <Icon
                      v-if="hasUnreadMessages"
                      name="tabler:message-circle-exclamation"
                      size="32"
                      color="blue"
                    />
                    <span>Сообщения</span>
                  </div>
                </a>

                <a
                  href="/favorites"
                  @click="closeMobileMenu"
                  class="w-full text-center text-white"
                >
                  <div class="flex items-center justify-center gap-2">
                    <Icon name="mdi:heart" size="32" />
                    <span>Избранное</span>
                  </div>
                </a>

                <button
                  @click="getSupport"
                  class="w-full text-center text-white"
                >
                  <div class="flex items-center justify-center gap-2">
                    <Icon
                      name="material-symbols:contact-support"
                      size="32"
                    ></Icon>
                    <span class="">Поддержка</span>
                  </div>
                </button>

                <a
                  href="/createProduct"
                  @click="closeMobileMenu"
                  class="bg-white text-blue-600 font-semibold py-3 px-6 rounded-full w-full text-center"
                >
                  Разместить объявление
                </a>
              </nav>
            </div>
          </div>
        </div>
      </header>
    </div>
    <main class="content">
      <slot></slot>
      <div v-if="showModal" class="modalWindow" @submit.prevent="sendMsg">
        <form class="modalForm relative">
          <h2 class="mb-5">Свяжитесь с нами</h2>
          <sub class="mb-10"
            >Ответ вы получите на свою почту в течение 2-3 дней</sub
          >
          <textarea v-model="msg" class="text-area" />
          <button type="submit" class="btn mt-10">Отправить</button>
          <button
            @click="showModal = false"
            class="absolute top-5 right-5 text-xl"
          >
            X
          </button>
        </form>
      </div>
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
      </div>
    </footer>
  </div>
</template>

<style lang="scss" scoped>
@use "~/assets/scss/main.scss" as main;

.head-links {
  @apply mx-auto ml-10 mr-20 mb-10 px-2 py-2 flex justify-between items-center;
}

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

  .logo-df {
    @apply flex justify-center items-center;
  }
}

.modalWindow {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
  animation: fadeIn 0.3s ease-in-out;
}

.modalForm {
  background-color: aliceblue;
  width: 60%;
  height: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  opacity: 80%;
  border-radius: 20px;
  h2 {
    font-size: 32px;
    text-align: center;
  }

  textarea {
    resize: none;
    width: 80%;
    height: 60%;
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

@media (max-width: 768px) {
  .mobile-menu-overlay {
    @apply fixed inset-0 bg-[#00569d] z-30 transform -translate-x-full transition-transform duration-300;

    &.open {
      @apply translate-x-0;
    }
  }

  .mobile-menu-content {
    @apply p-6 h-full w-full flex flex-col items-center justify-start;
  }

  .mobile-menu-button {
    @apply z-20;
  }

  .nav-link {
    @apply block py-4 text-white text-lg font-medium;
  }
}

@media (max-width: 620px) {
  .head-links {
    margin-left: 0 !important;
    margin-right: 0 !important;
  }
}
</style>
