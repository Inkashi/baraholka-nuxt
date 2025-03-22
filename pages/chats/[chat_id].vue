<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

const config = useRuntimeConfig();
const chat_id = useRoute().params.chat_id;
const messages = ref();
const userId = ref();
const apiBase = config.public.apiBase as string;
const isLoading = ref(true);
const user = ref();
const otherUser = ref();
let socket: WebSocket;
const photo_path = ref();

let title = "";
const newMessage = ref("");

const messagesList = ref<HTMLElement | null>(null);

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesList.value) {
      messagesList.value.scrollTop = messagesList.value.scrollHeight;
    }
  });
};

const fetchUserData = async () => {
  try {
    const token = useCookie<string | null>("auth_token").value;
    const decodedToken: any = jwtDecode(token!);

    userId.value = decodedToken.user_id || null;

    const response = await axios.get(`${apiBase}/api/getMessages/`, {
      params: { chat: chat_id },
      headers: {
        "Content-Type": "application/json",
      },
    });

    messages.value = response.data.messages || [];

    const getUsersByChat = await axios.get(`${apiBase}/api/getUsersByChat/`, {
      params: { chat: chat_id },
      headers: {
        "Content-Type": "application/json",
      },
    });

    const users = getUsersByChat.data;
    if (users.firstUser.id == userId.value) {
      user.value = users.firstUser;
      otherUser.value = users.secondUser;
    } else {
      user.value = users.secondUser;
      otherUser.value = users.firstUser;
    }

    photo_path.value = otherUser.value.photo;
    title = otherUser.value.name;
  } catch (error) {
    console.error("Ошибка при получении данных:", error);
  } finally {
    isLoading.value = false;
    scrollToBottom();
  }
};

onMounted(() => {
  socket = new WebSocket(`ws://localhost:8000/ws/chat/${chat_id}/`);
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    messages.value.push(data.message);
    scrollToBottom();
  };

  socket.onerror = (error) => {
    console.error("WebSocket error:", error);
  };
  fetchUserData();
});

onUnmounted(() => {
  // Закрываем соединение при размонтировании
  socket.close();
});

const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
};

const getUserPhoto = (message: any) => {
  return message.sender === userId.value
    ? user.value.photo
    : otherUser.value.photo;
};

const sendMessage = async () => {
  if (!newMessage.value.trim()) return;

  try {
    const response = await axios.post(`${apiBase}/api/getMessages/`, {
      sender: user.value.id,
      receiver: otherUser.value.id,
      message: newMessage.value,
    });

    if (response.status === 200) {
      scrollToBottom();
      newMessage.value = "";
    }
  } catch (error) {
    console.error("Ошибка при отправке сообщения:", error);
  }
};
</script>

<template>
  <div class="container">
    <loading v-if="isLoading"></loading>

    <div v-else class="chat-container">
      <div class="flex">
        <img :src="'/api' + photo_path" alt="User Photo" class="user-photo" />
        <h1 class="companion">{{ title }}</h1>
      </div>
      <div ref="messagesList" class="messages-list">
        <div v-for="message in messages" :key="message.id" class="message-item">
          <div :class="['message', { 'is-sender': message.sender === userId }]">
            <div class="message-content">
              <p>{{ message.message }}</p>
              <span class="time">{{ formatDate(message.sendingTime) }}</span>
            </div>
          </div>
        </div>
      </div>

      <form @submit.prevent="sendMessage" class="send-message-form">
        <input
          v-model="newMessage"
          type="text"
          placeholder="Ответить..."
          class="message-input"
        />
        <button type="submit" class="btn">Отправить</button>
      </form>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "~/assets/scss/main.scss" as main;
.companion {
  font-weight: bold;
  font-size: 24px;
  color: main.$second-color;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 70vh;
}

.messages-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  margin-bottom: 10px;
}

.message-item {
  display: flex;
  margin-bottom: 10px;
}

.message {
  display: flex;
  align-items: flex-start;
  max-width: 100%;
  padding: 10px;
  border-radius: 8px;
  background-color: main.$window-color;
  border: 1px solid main.$second-color;
  color: main.$second-color;
}

.message.is-sender {
  margin-left: auto;
  border: 1px solid main.$primary-color;
  color: main.$primary-color;
}

.user-photo {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 10px;
}

.message-content {
  display: flex;
  flex-direction: column;
  min-width: 180px;
  font-weight: 600;
}

.is-sender {
  .message-content {
    text-align: right;
  }
}

.message-content p {
  margin: 0;
  font-size: 18px;
}

.message-content .time {
  font-size: 10px;
  color: #666;
  margin-top: 5px;
}

.send-message-form {
  display: flex;
  gap: 10px;
  padding: 10px;
  border-top: 1px solid #ccc;
}

.message-input {
  flex: 1;
  padding: 10px;
  margin: 0;
  height: 100%;
  font-size: 18px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn {
  height: 100%;
}
</style>
