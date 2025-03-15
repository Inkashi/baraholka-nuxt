<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import { useRuntimeConfig } from "#app";

const config = useRuntimeConfig();
const userStore = useAuthStore();


const userId = ref<number | null>(null);
const isLoading = ref(true);
const chats = ref<any[]>([]);
const apiBase = config.public.apiBase as string;

const fetchUserData = async () => {
  try {
    const token = useCookie<string | null>("auth_token").value;
  
    const decodedToken: any = jwtDecode(token!);
    userId.value = decodedToken.user_id || null;
    
    if (userId.value) {
      const chatsResponse = await axios.get(`${apiBase}/api/getChats/`, {
        params: { user_id: userId.value },
        headers: {
          "Content-Type": "application/json",
        },
      });

      chats.value = chatsResponse.data.chats || [];
      console.log(chats.value)
    }
  } catch (error) {
    console.error("Ошибка при получении данных:", error);
  } finally {
    isLoading.value = false;
  }
};

const getUserPhoto = (chat: any) => {
  const otherUser = chat.firstUser.id === userId.value ? chat.secondUser : chat.firstUser;
  return otherUser.photo
};

const getUserName = (chat: any) => {
  const otherUser = chat.firstUser.id === userId.value ? chat.secondUser : chat.firstUser;
  return otherUser.name;
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

  <div v-else>
    <div v-if="chats.length > 0" class="chat-list">
      <div v-for="chat in chats" :key="chat.id" class="chat-item">
        <a :href="`/chats/${chat.id}`">
          <div class="chat-info"  >
          <div class="user-info">
            <img :src="getUserPhoto(chat)" alt="User Photo" class="user-photo" />
            <div class="user-details">
              <p class="user-name">{{ getUserName(chat) }}</p>
              <p class="last-message">{{ chat.lastMessage || 'Нет сообщений' }}</p>
            </div>
          </div>
        </div>
        </a>
      </div>
    </div>

    <div v-else>
      <p>Чаты не найдены</p>
    </div>
  </div>
</template>

<style lang="scss" scoped></style>
