<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import ProductModal from '../components/ProductModal.vue';

import notFavoriteIcon from '../assets/image/notFavorite.png';
import favoriteIcon from '../assets/image/favorite.png';

const config = useRuntimeConfig();
const products = ref([]);
const apiBase = config.public.apiBase as string;
const userId = ref();
const isLoading = ref(true);
const showModal = ref(false);
const selectedProduct = ref(null);
const favoriteCollection = ref([]);
const favorites = ref([]);
const search = ref('')
const cost = ref(-1)
const time = ref(-1)
const category = ref(null)
const sort = ref(0)

const openModal = (product) => {
    console.log(favorites.value)
    selectedProduct.value = product;
    showModal.value = true;
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
              userId:userId.value
            });

            favoriteCollection.value = response.data;

            const response2 = await axios.post(`${apiBase}/api/getFavorites/`, {
              favoriteCollection:favoriteCollection.value
            });

            favorites.value = response2.data;
            console.log(favorites.value)

        }
        catch (error) {
        console.error("Ошибка при получении данных:", error);
        } finally {
        isLoading.value = false;
        }
      };

// Функция для получения продуктов
const fetchProducts = async () => {
    try {
        const response = await axios.get(`${apiBase}/api/getProducts/`, {
            params: {
                userId: userId.value,
                start: 0,
                end: 10,
            },
        });

        products.value = response.data;
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
            favorites.value = favorites.value.filter((id) => id !== product.id)
        }
    } catch (error) {
        console.error("Ошибка при добавлении в избранное:", error);
    }
};

const getSearch = async () => {
    try {
        const formData = new FormData();
        formData.append('text', search.value);
        if (category.value) {
            formData.append('category', category.value);
        }
        if (sort.value) {
            formData.append('cost', String(cost.value));
        } else {
            formData.append('time', String(time.value));
        }
       
        const response = await axios.post(`${apiBase}/api/getSearched/`, formData);
        products.value = response.data;
    } catch (error) {
        console.error("Ошибка:", error);
    }
};


onMounted(() => {
    fetchUserData();
    getSearch();
});

</script>

<template>
  <div v-if="isLoading" class="loading">
        <div class="spinner"></div>
        <p>Загрузка...</p>
    </div>
  <div v-else class="center">
      <h1>Товары</h1>

      <!-- Поиск -->
      <input type="text"  v-model="search" @keyup.enter="getSearch" placeholder="Поиск..." />

      <!-- Список продуктов -->
      <div class="products-grid">
          <div v-for="product in products" :key="product.id" class="product-item" @click="openModal(product)">
              <img :src="product.picture" alt="Product Image" />
              <p>{{ product.title }}</p>
              <p>{{ product.cost }} руб.</p>
              <button class="favorite-button" @click.stop="addToFavorites(product)">
                        <img 
                            :src="isFavorite(product) ? favoriteIcon : notFavoriteIcon" 
                            alt="Favorite"
                        />
                </button>
          </div>
      </div>
      <ProductModal v-if="showModal" :showModal="showModal" :selectedProduct="selectedProduct" :favorites="favorites"
       :userId="userId" :secondUser="selectedProduct?.seller" @update:favorites="favorites = $event"  :favoriteCollection="favoriteCollection"
        @update:showModal="closeModal" />
        <select id="sort" v-model="sort" @change="getSearch" required>
                    <option :value=0>По времени</option>
                    <option :value=1>По цене</option>
        </select>
        <select v-if="!sort" id="time" v-model="time" @change="getSearch" required>
                    <option :value=-1></option>
                    <option :value=0>По возрастнию</option>
                    <option :value=1>По убыванию</option>
        </select>
        <select v-else id="cost" v-model="cost" @change="getSearch" required>
                    <option :value=-1></option>
                    <option :value=0>По возрастнию</option>
                    <option :value=1>По убыванию</option>
        </select>
  </div>
</template>

<style scoped>
.center {
    text-align: center;
}

.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 10px;
    margin-top: 20px;
}

.product-item {
    border: 1px solid #ccc;
    padding: 10px;
    text-align: center;
    position: relative; /* Для позиционирования сердечка */
}

.product-item img {
    max-width: 100%;
    height: auto;
}

.favorite-button {
    position: absolute;
    top: 5px;
    right: 5px;
    background-color: transparent;
    border: none;
    cursor: pointer;
    width: 24px; /* Установите фиксированную ширину */
    height: 24px; /* Установите фиксированную высоту */
    display: flex; /* Используйте flexbox для центрирования иконки */
    align-items: center;
    justify-content: center;
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