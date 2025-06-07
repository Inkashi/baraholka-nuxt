<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import ProductModal from "../components/ProductModal.vue";

import notFavoriteIcon from "../assets/image/notFavorite.png";
import favoriteIcon from "../assets/image/favorite.png";

const config = useRuntimeConfig();
const products = ref([]);
const apiBase = config.public.apiBase as string;
const userId = ref();
const isLoading = ref(true);
const showModal = ref(false);
const selectedProduct = ref(null);
const favoriteCollection = ref([]);
const favorites = ref([]);

const openModal = (product) => {
  if (product.status == 1) {
    selectedProduct.value = product;
    showModal.value = true;
  }
};

const closeModal = () => {
  showModal.value = false;
};

const fetchUserData = async () => {
  try {
    const token = useCookie<string | null>("auth_token").value;
    const decodedToken: any = jwtDecode(token!);

    userId.value = decodedToken.user_id || null;

    const response = await axios.post(`${apiBase}/api/getFavoriteCollection/`, {
      userId: userId.value,
    });

    favoriteCollection.value = response.data;
    console.log(favoriteCollection.value);

    const response2 = await axios.post(`${apiBase}/api/getFavorites/`, {
      favoriteCollection: favoriteCollection.value,
    });

    favorites.value = response2.data;

    fetchProducts();
  } catch (error) {
    console.error("Ошибка при получении данных:", error);
  } finally {
    isLoading.value = false;
  }
};

// Функция для получения продуктов
const fetchProducts = async () => {
  try {
    console.log(favoriteCollection.value);
    const response = await axios.get(`${apiBase}/api/getFavorites/`, {
      params: {
        favoriteCollection: favoriteCollection.value,
      },
    });

    products.value = response.data;
    console.log(products.value);
  } catch (error) {
    console.error("Ошибка при получении продуктов:", error);
  }
};

// Проверка, добавлен ли продукт в избранное
const isFavorite = (product) => {
  return favorites.value.includes(product.id);
};

// Добавление продукта в избранное
const addToFavorites = async (product) => {
  try {
    const response = await axios.post(`${apiBase}/api/addFavorite/`, {
      favoriteCollection: favoriteCollection.value,
      productId: product.id,
    });

    if (response.status === 200) {
      favorites.value.push(product.id); // Добавляем ID продукта в массив favorites
    } else if (response.status === 202) {
      favorites.value = favorites.value.filter((id) => id !== product.id);
    }
  } catch (error) {
    console.error("Ошибка при добавлении в избранное:", error);
  }
};

onMounted(() => {
  fetchUserData();
});
</script>

<template>
  <div class="container">
    <loading v-if="isLoading"></loading>
    <div v-else class="center">
      <h1 class="title">Отложенные</h1>

      <div class="products-grid">
        <div
          v-for="product in products"
          :key="product.id"
          class="product-item"
          :class="{ inactive: product.status != 1 }"
          @click="openModal(product)"
        >
          <img :src="'/api/pictures' + product.picture" alt="Product Image" />
          <div class="product-info">
            <p>{{ product.title }}</p>
            <p>{{ product.cost }} руб.</p>
          </div>
          <button
            v-if="userId"
            class="favorite-button"
            @click.stop="addToFavorites(product)"
          >
            <img
              :src="isFavorite(product) ? favoriteIcon : notFavoriteIcon"
              alt="Favorite"
            />
          </button>
          <div v-if="product.status != 1" class="status-overlay">
            {{ product.statusText }}
          </div>
        </div>
      </div>
      <ProductModal
        v-if="showModal"
        :showModal="showModal"
        :selectedProduct="selectedProduct"
        :favorites="favorites"
        :userId="userId"
        :secondUser="selectedProduct?.seller"
        @update:favorites="favorites = $event"
        :favoriteCollection="favoriteCollection"
        @update:showModal="closeModal"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "~/assets/scss/main.scss" as main;

.center {
  text-align: center;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 2%;

  @media (max-width: 768px) {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
}

.title {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 10px;
  color: main.$primary-color;
}

.product-item {
  position: relative;
  border-radius: 5px;
  border: 2px solid rgba(83, 76, 76, 0.185);

  &:hover {
    transform: scale(1.02);
  }

  img {
    width: 100%;
    height: 280px;
    border-radius: 5px 5px 0 0;
    object-fit: cover;

    @media (max-width: 768px) {
      height: 150px; /* Уменьшаем высоту изображений */
    }
  }

  .product-info {
    background-color: rgba(white, 0.6);
    border-radius: 0 0 5px 5px;
    text-align: left;
    padding: 10px;

    .card-title {
      font-size: 18px;
      font-weight: bold;
      color: main.$primary-color;
      margin-bottom: 1px;

      @media (max-width: 768px) {
        font-size: 14px; /* Уменьшаем размер текста */
      }
    }

    .card-cost {
      font-size: 18px;
      color: main.$second-color;
      letter-spacing: 1px;
      font-weight: bold;

      @media (max-width: 768px) {
        font-size: 14px; /* Уменьшаем размер текста */
      }
    }
  }

  .favorite-button {
    z-index: 2;
    position: absolute;
    top: 10px;
    right: 10px;
    background: transparent;
    border: none;
    cursor: pointer;
    width: 30px;
    height: 30px;

    img {
      width: 100%;
      height: 100%;
    }
  }
}

.status-overlay {
  position: absolute;
  top: 1%;
  left: 3%;
  padding: 10px;
  color: white;
  font-size: 18px;
  font-weight: bold;
  z-index: 2;
  text-align: center;
  pointer-events: none;
}

.status-overlay::before {
  content: "";
  position: absolute;
  top: 7%;
  left: 0;
  width: 100%;
  height: 80%;
  background-color: rgba(0, 0, 0, 0.562);
  border-radius: 5px;
  z-index: -1;
}

.product-item.inactive::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(128, 128, 128, 0.5);
  z-index: 1;
}

.product-item.inactive:hover {
  transform: scale(1);
}

.fa-heart {
  width: 20px;
  height: 20px;
  font-size: 20px; /* Размер иконки */
  color: red; /* Цвет иконки */
}

.fa-solid {
  font-weight: bold;
}
</style>
