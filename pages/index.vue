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
const userId = ref<number | null>(null);
const isLoading = ref(true);
const showModal = ref(false);
const selectedProduct = ref(null);
const favoriteCollection = ref([]);
const favorites = ref<number[]>([]);
const search = ref("");
const category = ref<number | null>(null);
const sortOption = ref<string>("new");

const isCategoryDropdownOpen = ref(false);
const isSortDropdownOpen = ref(false);

const selectedCategory = ref<{ id: number; title: string } | null>(null);
const selectedSortOption = ref<string | null>(null);

// Категории
const categories = ref([
  { id: 0, title: "Все" },
  { id: 1, title: "Одежда" },
  { id: 2, title: "Услуги" },
  { id: 3, title: "Электроника" },
  { id: 4, title: "Работа" },
  { id: 5, title: "Разное" },
]);

const toggleCategoryDropdown = () => {
  isCategoryDropdownOpen.value = !isCategoryDropdownOpen.value;
};

const toggleSortDropdown = () => {
  isSortDropdownOpen.value = !isSortDropdownOpen.value;
};

const selectCategory = (cat: { id: number; title: string }) => {
  category.value = cat.id;
  isCategoryDropdownOpen.value = false;
  getSearch();
};

const selectSortOption = (option: string) => {
  sortOption.value = option;
  isSortDropdownOpen.value = false;
  getSearch();
};

// Открытие модального окна
const openModal = (product) => {
  selectedProduct.value = product;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

// Получение данных пользователя
const fetchUserData = async () => {
  const token = useCookie<string | null>("auth_token").value;
  if (!token) {
    isLoading.value = false;
    return;
  }

  try {
    const token = useCookie<string | null>("auth_token").value;
    const decodedToken: any = jwtDecode(token!);

    userId.value = decodedToken.user_id || null;

    const response = await axios.post(`${apiBase}/api/getFavoriteCollection/`, {
      userId: userId.value,
    });

    favoriteCollection.value = response.data;

    const response2 = await axios.post(`${apiBase}/api/getFavorites/`, {
      favoriteCollection: favoriteCollection.value,
    });

    favorites.value = response2.data;
    console.log(favorites.value);
  } catch (error) {
    console.error("Ошибка при получении данных:", error);
  } finally {
    isLoading.value = false;
  }
};

// Получение продуктов
const fetchProducts = async () => {
  try {
    const response = await axios.get(`${apiBase}/api/getProducts/`, {
      params: { userId: userId.value, start: 0, end: 10 },
    });
    products.value = response.data;
  } catch (error) {
    console.error("Ошибка при получении продуктов:", error);
  }
};

// Проверка избранного
const isFavorite = (product) => {
  return favorites.value.includes(product.id);
};

// Добавление в избранное
const addToFavorites = async (product) => {
  try {
    const response = await axios.post(`${apiBase}/api/addFavorite/`, {
      favoriteCollection: favoriteCollection.value,
      productId: product.id,
    });

    if (response.status === 200) {
      favorites.value.push(product.id);
    } else if (response.status === 202) {
      favorites.value = favorites.value.filter((id) => id !== product.id);
    }
  } catch (error) {
    console.error("Ошибка при добавлении в избранное:", error);
  }
};

// Поиск
const getSearch = async () => {
  try {
    const formData = new FormData();
    formData.append("text", search.value);
    if (category.value) formData.append("category", String(category.value));
    if (sortOption.value === "Сначала старые") formData.append("time", "0");
    else if (sortOption.value === "Сначала новые") formData.append("time", "1");
    else if (sortOption.value === "Сначала дешевые")
      formData.append("cost", "0");
    else if (sortOption.value === "Сначала дорогие")
      formData.append("cost", "1");

    const response = await axios.post(`${apiBase}/api/getSearched/`, formData);
    products.value = response.data;
  } catch (error) {
    console.error("Ошибка:", error);
  }
};

const handleClickOutside = (event: MouseEvent) => {
  const dropdownElement = document.querySelector(".category-selector");
  const dropdownElement2 = document.querySelector(".sort-selector");
  if (dropdownElement && !dropdownElement.contains(event.target as Node)) {
    isCategoryDropdownOpen.value = false;
  }
  if (dropdownElement2 && !dropdownElement2.contains(event.target as Node)) {
    isSortDropdownOpen.value = false;
  }
};

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});

onMounted(() => {
  fetchUserData();
  getSearch();
  document.addEventListener("click", handleClickOutside);
});
</script>

<template>
  <loading v-if="isLoading"></loading>
  <div v-else class="container">
    <div class="center">
      <div class="search-bar">
        <div class="category-selector">
          <button class="category-button" @click="toggleCategoryDropdown">
            {{
              selectedCategory ? selectedCategory.title : "Выбрать категорию"
            }}
          </button>
          <ul v-if="isCategoryDropdownOpen" class="category-dropdown">
            <li
              v-for="cat in categories"
              :key="cat.id"
              @click="selectCategory(cat)"
            >
              {{ cat.title }}
            </li>
          </ul>
        </div>

        <div class="category-selector sort-selector">
          <button class="category-button" @click="toggleSortDropdown">
            {{ selectedSortOption || "Сортировать" }}
          </button>
          <ul v-if="isSortDropdownOpen" class="category-dropdown">
            <li @click="selectSortOption('Сначала старые')">Сначала старые</li>
            <li @click="selectSortOption('Сначала новые')">Сначала новые</li>
            <li @click="selectSortOption('Сначала дешевые')">
              Сначала дешевые
            </li>
            <li @click="selectSortOption('Сначала дорогие')">
              Сначала дорогие
            </li>
          </ul>
        </div>

        <div class="search-input">
          <input
            type="text"
            v-model="search"
            @keyup.enter="getSearch"
            placeholder="Поиск..."
          />
          <button @click="getSearch">Найти</button>
        </div>
      </div>

      <div class="products-grid">
        <div
          v-for="product in products"
          :key="product.id"
          class="product-item"
          @click="openModal(product)"
        >
          <img :src="product.picture" alt="Product Image" />
          <div class="product-info">
            <p class="card-title">{{ product.title }}</p>
            <p class="card-cost">{{ product.cost }} ₽</p>
          </div>
          <button class="favorite-button" @click.stop="addToFavorites(product)">
            <img
              :src="isFavorite(product) ? favoriteIcon : notFavoriteIcon"
              alt="Favorite"
            />
          </button>
        </div>
      </div>

      <!-- Модальное окно -->
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
@use "sass:color";

:root {
  --bg-color: #f9f9f9;
  --gap: 20px;
}

.center {
  text-align: center;
}

.category-selector {
  position: relative;
  display: inline-block;

  .category-button {
    padding: 10px 20px;
    background-color: main.$second-color;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 16px;
    color: white;
    font-weight: bold;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: background-color 0.3s ease;

    &:hover {
      background-color: #e0e0e0;
    }

    .icon {
      margin-left: 10px;
      font-size: 12px;
    }
  }

  .category-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    background-color: color.scale(
      main.$window-color,
      $lightness: +15%,
      $alpha: -10%
    );
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    z-index: 10;
    list-style: none;
    margin: 0;
    padding: 0;
    overflow: hidden;

    li {
      padding: 10px;
      cursor: pointer;
      transition: background-color 0.3s ease;

      &:hover {
        background-color: #f0f0f0;
      }
    }
  }
}

.search-bar {
  display: flex;
  gap: var(--gap);
  margin-bottom: 20px;
  flex-wrap: wrap;

  @media (max-width: 768px) {
    flex-direction: column;
    align-items: stretch;
  }
}

.search-input {
  flex: 1;
  min-width: 200px;
  display: flex;
  border-radius: 5px;

  input {
    width: 80%;
    font-weight: 600;
    height: auto;
    margin: 0;
    border: 2px solid main.$second-color;
    border-radius: 5px 0 0 5px;

    &::placeholder {
      color: main.$second-color;
    }

    @media (max-width: 768px) {
      width: 100%;
      height: 50px;
    }
  }

  button {
    background-color: main.$second-color;
    font-weight: bold;
    color: white;
    border-radius: 0 5px 5px 0;
    width: 20%;
    transition: all 0.5s;

    &:hover {
      font-size: 18px;
      color: rgb(198, 198, 255);
    }

    @media (max-width: 768px) {
      width: 100%; /* На маленьких экранах занимает всю ширину */
      height: 50px;
      border-radius: 5px; /* Убираем скругление только справа */
    }
  }

  @media (max-width: 768px) {
    flex-direction: column; /* На маленьких экранах делаем вертикальное расположение */
  }
}

/* Сетка товаров */
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 2%;

  @media (max-width: 768px) {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
}

.product-item {
  position: relative;
  border-radius: 5px;

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
</style>
