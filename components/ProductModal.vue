<script setup lang="ts">
import axios from "axios";

import notFavoriteIcon from "../assets/image/notFavorite.png";
import favoriteIcon from "../assets/image/favorite.png";

const config = useRuntimeConfig();

const apiBase = config.public.apiBase as string;

const emit = defineEmits(["update:showModal", "update:favorites"]);

const props = defineProps({
  showModal: Boolean,
  selectedProduct: Object,
  userId: Number,
  secondUser: Number,
  favorites: Array,
  favoriteCollection: Number,
});

const handleOverlayClick = (event: MouseEvent) => {
  const modalContent = document.querySelector(".modal-content");
  if (modalContent && !modalContent.contains(event.target as Node)) {
    closeModal();
  }
};

const closeModal = () => {
  emit("update:showModal", false);
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
      emit("update:favorites", updatedFavorites);
    } else if (response.status === 202) {
      const updatedFavorites = props.favorites.filter(
        (id) => id !== props.selectedProduct.id
      );
      emit("update:favorites", updatedFavorites);
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
  <div v-if="showModal" class="modal-overlay" @click="handleOverlayClick">
    <div class="modal-content">
      <h1 class="modal-title">{{ selectedProduct.title }}</h1>
      <button @click="closeModal" class="close-button">✕</button>
      <div class="flex w-full">
        <div class="product-image-container">
          <img
            :src="selectedProduct.picture"
            alt="Product Image"
            class="product-image"
          />
        </div>
        <div class="product-details flex flex-col text-left ml-6">
          <p><strong>Описание:</strong></p>
          <p>{{ selectedProduct.description }}</p>
          <p>
            <strong>Цена: </strong>
            <span class="price">{{ selectedProduct.cost }} руб.</span>
          </p>
        </div>
      </div>
      <!-- Кнопки действий -->
      <div class="action-buttons">
        <button class="favorite-button" @click.stop="addToFavorites">
          <img
            :src="isFavorite() ? favoriteIcon : notFavoriteIcon"
            alt="Favorite"
            class="favorite-icon"
          />
        </button>
        <button class="contact-button" @click="getChat">
          Связаться с продавцом
        </button>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "~/assets/scss/main.scss" as main;

.modal-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 15px;
}

.modal-overlay {
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

.modal-content {
  background-color: main.$window-color;
  padding: 24px;
  border-radius: 12px;
  max-width: 700px;
  width: 100%;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  position: relative;
  animation: scaleUp 0.3s ease-in-out;
}

/* Анимация появления фона */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Анимация увеличения контента */
@keyframes scaleUp {
  from {
    transform: scale(0.9);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

/* Кнопка закрытия */
.close-button {
  position: absolute;
  top: 12px;
  right: 12px;
  background: none;
  border: none;
  font-size: 24px;
  color: #aaa;
  cursor: pointer;
  transition: color 0.3s ease;
}

.close-button:hover {
  color: #ff4d4d;
}

/* Заголовок */
.product-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 16px;
  text-align: center;
  color: #333;
}

/* Изображение продукта */
.product-image-container {
  display: flex;
  height: 260px;
  width: auto;
  justify-content: center;
  margin-bottom: 16px;
}

.product-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Детали продукта */
.product-details {
  margin-bottom: 24px;
  line-height: 1.6;
  color: black;
  width: 70%;
  p {
    font-size: 20px;
    width: 100%;
  }
}

/* Кнопки действий */
.action-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.favorite-button {
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.favorite-button:hover {
  background-color: #f0f0f0;
}

.favorite-icon {
  width: 24px;
  height: 24px;
}

.contact-button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.contact-button:hover {
  background-color: #2980b9;
}
</style>
