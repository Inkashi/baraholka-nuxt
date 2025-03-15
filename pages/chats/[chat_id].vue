<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

const config = useRuntimeConfig();
const chat_id = useRoute().params.chat_id;
const messages = ref([]);
const userId = ref<number | null>(null);
const apiBase = config.public.apiBase as string;
const isLoading = ref(true);
const user = ref<any>(null);
const otherUser = ref<any>(null);
let socket: WebSocket;
let title = '';
const newMessage = ref("");
const messagesList = ref<HTMLElement | null>(null);

// Прокрутка вниз
const scrollToBottom = () => {
    if (messagesList.value) {
        messagesList.value.scrollTop = messagesList.value.scrollHeight;
    }
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
        title = otherUser.value.name;
    } catch (error) {
        console.error("Ошибка при получении данных:", error);
    } finally {
        isLoading.value = false;
        scrollToBottom(); // Прокрутка вниз после загрузки данных
    }
};

onMounted(() => {
    socket = new WebSocket(`ws://localhost:8000/ws/chat/${chat_id}/`);
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        messages.value.push(data.message);
        scrollToBottom(); // Прокрутка вниз при получении нового сообщения
    };

    // Обработка ошибок
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
    return message.sender === userId.value ? user.value.photo : otherUser.value.photo;
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
            newMessage.value = "";
            scrollToBottom(); // Прокрутка вниз после отправки сообщения
        }
    } catch (error) {
        console.error("Ошибка при отправке сообщения:", error);
    }
};
</script>

<template>
    <div v-if="isLoading" class="loading">
        <div class="spinner"></div>
        <p>Загрузка...</p>
    </div>

    <div v-else class="chat-container">
        <h1>{{ title }}</h1>

        <!-- Список сообщений -->
        <div ref="messagesList" class="messages-list">
            <div v-for="message in messages" :key="message.id" class="message-item">
                <div :class="['message', { 'is-sender': message.sender === userId }]">
                    <img v-if="message.sender !== userId" :src="getUserPhoto(message)" alt="User Photo" class="user-photo" />
                    <div class="message-content">
                        <p>{{ message.message }}</p>
                        <span class="time">{{ formatDate(message.sendingTime) }}</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Форма для отправки сообщений -->
        <form @submit.prevent="sendMessage" class="send-message-form">
            <input v-model="newMessage" type="text" placeholder="Ответить..." class="message-input" />
            <button type="submit" class="send-button">Отправить</button>
        </form>
    </div>
</template>

<style scoped>
.chat-container {
    display: flex;
    flex-direction: column;
    height: 100vh; /* Занимает всю высоту экрана */
}

.messages-list {
    flex: 1; /* Занимает всё доступное пространство */
    overflow-y: auto; /* Добавляет вертикальную прокрутку */
    padding: 10px;
    border: 1px solid #ccc;
    margin-bottom: 10px;
}

.message-item {
    display: flex;
    margin-bottom: 10px;
}

.message {
    display: flex;
    align-items: flex-start;
    max-width: 70%;
    padding: 10px;
    border-radius: 8px;
    background-color: #f0f0f0;
}

.message.is-sender {
    margin-left: auto; /* Сообщения отправителя выравниваются по правому краю */
    background-color: #dcf8c6; /* Цвет фона для отправителя */
}

.user-photo {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
    margin-right: 10px;
}

.message-content {
    display: flex;
    flex-direction: column;
}

.message-content p {
    margin: 0;
    font-size: 14px;
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
    border: 1px solid #ccc;
    border-radius: 4px;
}

.send-button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.send-button:hover {
    background-color: #0056b3;
}
</style>