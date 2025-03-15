<script setup lang="ts">
    import { ref, onMounted } from "vue";
    import axios from "axios";
    import { jwtDecode } from "jwt-decode";

    const config = useRuntimeConfig()
    const chat_id = useRoute().params.chat_id
    const messages = ref();
    const userId = ref()
    const apiBase = config.public.apiBase as string;
    const isLoading = ref(true);
    const user = ref();
    const otherUser = ref();
    let socket: WebSocket;
    let title = '';
    const newMessage = ref("");

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
            if (users.firstUser.id == userId) {
                user.value = users.firstUser
                otherUser.value = users.secondUser
            } else {
                user.value = users.secondUser
                otherUser.value = users.firstUser
            }
            title = otherUser.value.name
            
        }
        catch (error) {
        console.error("Ошибка при получении данных:", error);
        } finally {
        isLoading.value = false;
        }


    };

    onMounted(() => {
    socket = new WebSocket(`ws://localhost:8000/ws/chat/${chat_id}/`);
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        messages.value.push(data.message);
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
        <div class="messages-list">
            <div v-for="message in messages" :key="message.id" class="message-item">
                <div :class="['message', { 'is-sender': message.sender === userId }]">
                    <img :src="getUserPhoto(message)" alt="User Photo" class="user-photo" />
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

<style lang="scss" scoped></style>
