<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";

import notFavoriteIcon from '../assets/image/notFavorite.png';
import favoriteIcon from '../assets/image/favorite.png';

const config = useRuntimeConfig();

const apiBase = config.public.apiBase as string;

const emit = defineEmits(['update:showModal', 'update:favorites']);

const props = defineProps({
    showModal: Boolean,
    selectedProduct: Object,
    userId: Number,
    secondUser: Number,
    favorites: Array, 
    favoriteCollection: Number,
});

const closeModal = () => {
    emit('update:showModal', false);
};

const getChat = async () => {
    try {
        const response = await axios.post(`${apiBase}/api/getChatByUsers/`, {
            firstUser: props.userId,
            secondUser: props.secondUser,
        });

        const chat_id = response.data; 
        navigateTo(`/chats/${chat_id}`);
    } catch (error) {
        console.error("Ошибка при создании чата:", error);
    }
};

const addToFavorites = async () => {
    try {
        const response = await axios.post(`${apiBase}/api/addFavorite/`, {
            favoriteCollection: props.favoriteCollection,
            productId: props.selectedProduct.id,
        });

        if (response.status === 200) {
            const updatedFavorites = [...props.favorites, props.selectedProduct.id];
            emit('update:favorites', updatedFavorites);
        } else if (response.status === 202) {
            const updatedFavorites = props.favorites.filter((id) => id !== props.selectedProduct.id);
            emit('update:favorites', updatedFavorites);
        }
    } catch (error) {
        console.error("Ошибка при добавлении в избранное:", error);
    }
};

const isFavorite = () => {
    return props.favorites.includes(props.selectedProduct.id);
};

</script>

<template>
    <div v-if="showModal" class="modal-overlay">
        <div class="modal-content">
            <button @click="closeModal" class="close-button">X</button>
            <h2>{{ selectedProduct.title }}</h2>
            <img :src="selectedProduct.picture" alt="Product Image" />
            <p><strong>Описание:</strong> {{ selectedProduct.description }}</p>
            <p><strong>Цена:</strong> {{ selectedProduct.cost }} руб.</p>
            <button class="favorite-button" @click.stop="addToFavorites">
                        <img 
                            :src="isFavorite() ? favoriteIcon : notFavoriteIcon" 
                            alt="Favorite"
                        />
                </button>
            <button @click=getChat>
                Связаться с продавцом
            </button>
            
        </div>
    </div>
</template>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
}

.modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    max-width: 600px;
    position: relative;
}

.close-button {
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: red;
    color: white;
    border: none;
    cursor: pointer;
    padding: 5px 10px;
    border-radius: 4px;
}

.favorite-button {
    position: absolute;
    top: 5px;
    left: 5px;
    background-color: transparent;
    border: none;
    cursor: pointer;
    width: 24px; /* Установите фиксированную ширину */
    height: 24px; /* Установите фиксированную высоту */
    display: flex; /* Используйте flexbox для центрирования иконки */
    align-items: center;
    justify-content: center;
}
</style>