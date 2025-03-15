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
    userPhoto.value = userData.photoPath || null;
  } catch (error) {
    console.error("Ошибка при получении данных пользователя:", error);
  } finally {
    isLoading.value = false;
  }
};

const handleLogout = () => {
  userStore.logoutUser();
};

const handleImageUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    const isConfirmed = window.confirm(
      "Вы уверены, что хотите сменить фотографию?"
    );
    if (!isConfirmed) {
      return;
    }

    const file = target.files[0];
    const formData = new FormData();

    formData.append('user_id', userId.value);
    formData.append('photo', file);

    try {
      const response = await axios.post(`${apiBase}/api/changeUser/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.status === 200) {
        userPhoto.value = response.data.photoPath;
      }
    } catch (error) {
      console.error("Ошибка при загрузке фотографии:", error);
    }
  }
};

onMounted(() => {
  fetchUserData();
});
</script>

<template>
  <div v-if="isLoading" class="loading">
    <div class="spinner"></div>
    <p>Загрузка...</p>
  </div>
  <div v-else class="userInfo">
    <div class="flex justify-center items-center">
      <div class="userImage" @click="() => $refs.fileInput.click()">
        <img
          v-if="userPhoto"
          :src="userPhoto"
          alt="Фото пользователя"
          class="profile-image"
        />
        <div v-else class="placeholder">Добавить фото</div>
        <input
          type="file"
          accept="image/*"
          style="display: none"
          ref="fileInput"
          @change="handleImageUpload"
        />
      </div>

      <div class="ml-10">
        <h2>{{ userName }}</h2>
        <h2>{{ userEmail }}</h2>
      </div>

      <div>
        <button class="btn" @click="handleLogout">Выйти</button>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "~/assets/scss/main.scss" as main;
@use "sass:color";

.userInfo {
  width: 80%;
  background-color: color.scale(
    main.$window-color,
    $lightness: +15%,
    $alpha: -10%
  );
  border-radius: 5px;
  margin-top: 10%;
  margin-left: 10%;
  height: max-content;
  position: relative;
  display: flex;
  align-items: center;
  padding: 1%;
  gap: 20px;
}

.userImage {
  width: 13vw;
  height: 28vh;
  border-radius: 5%;
  overflow: hidden;
  cursor: pointer;
  background-color: #ccc;
  display: flex;
  align-items: center;
  justify-content: center;
}

.profile-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder {
  font-size: 14px;
  color: #666;
}

.btn {
  position: absolute;
  right: 2%;
  top: 5%;
  width: 10vw;
  height: 4vh;
  background-color: rgba(255, 0, 0, 0.651);
  transition: all 1s;

  &:hover {
    background-color: rgb(255, 0, 0);
    transform: scale(0.95);
  }
}

h2 {
  font-size: 24px;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  position: absolute;
  background-color: transparent;
  top: 0;
  left: 0;
  z-index: 10;

  .spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-left-color: #3498db;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
  }

  p {
    margin-left: 10px;
    font-size: 18px;
    color: #333;
    font-weight: bold;
  }
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
