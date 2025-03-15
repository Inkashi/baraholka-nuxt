<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";
const config = useRuntimeConfig();

const userName = ref("Имя пользователя");
const userId = ref();
const userEmail = ref("email@example.com");
const userPhoto = ref<string | null>(null);
const isLoading = ref(true);
const userStore = useAuthStore();
const apiBase = config.public.apiBase as string;

const fetchUserData = async () => {
  try {
    const token = useCookie<string | null>("auth_token").value;
    if (!token) {
      console.error("Токен не найден");
      return;
    }

    const response = await axios.get(`${apiBase}/api/getUser/`, {
      params: { token },
      headers: {
        "Content-Type": "application/json",
      },
    });

    const userData = response.data;
    userId.value = userData.id;
    userName.value = userData.name || "Неизвестное имя";
    userEmail.value = userData.email || "Неизвестный email";
    userPhoto.value = userData.photo || null;
  } catch (error) {
    console.error("Ошибка при получении данных пользователя:", error);
  } finally {
    isLoading.value = false;
  }

    const response = await axios.get(`${apiBase}/api/getChats/`, {
      params: { user_id: 1 },
      headers: {
        "Content-Type": "application/json",
      },
    });

    console.log(response.data)

};

onMounted(() => {
  fetchUserData();
});
</script>

<template>
  <div class="center">Тут будет основная страница</div>
</template>

<style lang="scss" scoped></style>
