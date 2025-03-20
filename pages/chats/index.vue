<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import { useRuntimeConfig } from "#app";

const config = useRuntimeConfig();
const userStore = useAuthStore();
const apiBase = config.public.apiBase as string;

// Состояния
const isLoading = ref(true);
const chats = ref<any[]>([]);
const userId = ref<number | null>(null);
const lastMsgUser = ref<number | null>(null);
const webSockets = new Map<number, WebSocket>(); // Хранилище WebSocket соединений

// Получение данных о чатах
const fetchUserData = async () => {
  try {
    const token = useCookie<string | null>("auth_token").value;
    const decodedToken: any = jwtDecode(token!);
    userId.value = decodedToken.user_id || null;

    if (userId.value) {
      const chatsResponse = await axios.get(`${apiBase}/api/getChats/`, {
        params: { user_id: userId.value },
        headers: { "Content-Type": "application/json" },
      });

      chats.value = chatsResponse.data.chats || [];
      lastMsgUser.value =
        chats.value.length > 0 ? chats.value[0].user_id : null; // Устанавливаем последнего пользователя из первого чата
    }
  } catch (error) {
    console.error("Ошибка при получении данных:", error);
  } finally {
    isLoading.value = false;
  }
};

// Открытие WebSocket для конкретного чата
const openWebSocket = (chatId: number) => {
  const socket = new WebSocket(`ws://localhost:8000/ws/chat/${chatId}/`);

  socket.onopen = () => {
    console.log(`WebSocket opened for chat ${chatId}`);
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    const chat = chats.value.find((c) => c.id === chatId);
    if (chat) {
      chat.lastMessage = data.message.message; // Обновляем последнее сообщение
    }

    console.log(`Message received for chat ${chatId}:`, data);
  };

  socket.onerror = (error) => {
    console.error(`WebSocket error for chat ${chatId}:`, error);
  };

  socket.onclose = () => {
    console.log(`WebSocket closed for chat ${chatId}`);
    webSockets.delete(chatId); // Удаляем закрытое соединение из хранилища
  };

  webSockets.set(chatId, socket); // Сохраняем соединение в хранилище
};

// Закрытие WebSocket для конкретного чата
const closeWebSocket = (chatId: number) => {
  const socket = webSocks.get(chatId);
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.close();
  }
};

// Закрытие всех WebSocket соединений
const closeAllWebSockets = () => {
  webSockets.forEach((socket, chatId) => {
    if (socket.readyState === WebSocket.OPEN) {
      socket.close();
    }
    webSockets.delete(chatId);
  });
};

// Получение фото пользователя из чата
const getUserPhoto = (chat: any) => {
  const otherUser =
    chat.firstUser.id === userId.value ? chat.secondUser : chat.firstUser;
  return otherUser.photo;
};

// Получение имени пользователя из чата
const getUserName = (chat: any) => {
  const otherUser =
    chat.firstUser.id === userId.value ? chat.secondUser : chat.firstUser;
  return otherUser.name;
};

// Определение цвета сообщения
const msgColor = () => {
  return userId.value === lastMsgUser.value ? "greenText" : "blueText";
};

onMounted(() => {
  fetchUserData();

  // Открываем WebSocket для каждого чата после загрузки данных
  setTimeout(() => {
    chats.value.forEach((chat) => {
      openWebSocket(chat.id);
    });
  }, 1000); // Добавляем задержку для завершения загрузки данных
});

onUnmounted(() => {
  // Закрываем все WebSocket соединения при размонтировании компонента
  closeAllWebSockets();
});
</script>

<template>
  <div class="container">
    <loading v-if="isLoading"></loading>

    <div v-else>
      <div v-if="chats.length > 0" class="chat-list">
        <div v-for="chat in chats" :key="chat.id" class="chat-item">
          <a :href="`/chats/${chat.id}`">
            <div class="chat-info">
              <div class="user-info">
                <img
                  :src="getUserPhoto(chat)"
                  alt="User Photo"
                  class="user-photo"
                />
                <div class="user-details">
                  <p class="user-name">{{ getUserName(chat) }}</p>
                  <p class="last-message" :class="msgColor()">
                    {{ chat.lastMessage || "Нет сообщений" }}
                  </p>
                </div>
              </div>
            </div>
          </a>
        </div>
      </div>

      <div v-else class="noChats">
        <p>Вы не начинали чатиксы с другими людьми</p>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "~/assets/scss/main.scss" as main;

.noChats {
  width: 100%;
  height: 20vh;
  background-color: main.$window-color;
  border: 2px solid main.$second-color;
  display: flex;
  justify-content: center;
  align-items: center;
  p {
    font-size: 32px;
    font-weight: bold;
    color: main.$primary-color;
  }
}

.user-photo {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  padding: 5px;
}

.blueText {
  color: main.$primary-color;
}

.greenText {
  color: main.$second-color;
}

.chat-info {
  width: 100%;
  background-color: main.$window-color;
  border: 2px solid main.$second-color;
}

.user-info {
  width: 100%;
  display: flex;

  .user-details {
    padding-left: 10px;

    .user-name {
      font-size: 24px;
      color: main.$second-color;
      font-weight: bold;
    }

    .last-message {
      font-size: 18px;
      font-weight: 600;
    }
  }
}
</style>
