<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";

import editIcon from "../assets/image/edit.png";

const config = useRuntimeConfig();

const isEdit = ref(false);
const newName = ref("");
const userName = ref("Имя пользователя");
const userId = ref();
const userEmail = ref("email@example.com");
const userPhoto = ref<string | null>(null);
const isLoading = ref(true);
const products = ref([]);
const statuses = ref([]);
const status = ref([]);

const productStatuses = ref({});
const userStore = useAuthStore();
const apiBase = config.public.apiBase as string;
const buttonText = ref("Изменить имя");
const fetchStatuses = async () => {
  try {
    const response = await axios.get(`${apiBase}/api/getStatuses/`);
    statuses.value = response.data;
  } catch (error) {
    console.error("Ошибка при получении категорий:", error);
  }
};

const fetchUserData = async () => {
  try {
    const token = useCookie<string | null>("auth_token").value;
    if (!token) {
      console.error("Токен не найден");
      return;
    }

    const response = await axios.get(`${apiBase}/api/getUser/`, {
      params: { token },
      headers: {
        "Content-Type": "application/json",
      },
    });

    const userData = response.data;
    userId.value = userData.id;
    userName.value = userData.name || "Неизвестное имя";
    userEmail.value = userData.email || "Неизвестный email";
    userPhoto.value = userData.photoPath || null;
    fetchProducts();
  } catch (error) {
    console.error("Ошибка при получении данных пользователя:", error);
  } finally {
    isLoading.value = false;
  }
};

const handleLogout = () => {
  userStore.logoutUser();
};

const handleImageUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    const isConfirmed = window.confirm(
      "Вы уверены, что хотите сменить фотографию?"
    );
    if (!isConfirmed) {
      return;
    }

    const file = target.files[0];
    const formData = new FormData();

    formData.append("user_id", userId.value);
    formData.append("photo", file);

    try {
      const response = await axios.post(
        `${apiBase}/api/changeUser/`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      if (response.status === 200) {
        userPhoto.value = response.data.photo;
      }
    } catch (error) {
      console.error("Ошибка при загрузке фотографии:", error);
    }
  }
};

const changeBtn = (event: Event) => {
  const btn = event.target as HTMLButtonElement;
  isEdit.value = true;
  buttonAction.value = changeName;
  buttonText.value = "Изменить";
};
const buttonAction = ref(changeBtn);
const changeName = async () => {
  if (newName.value !== "") {
    const formData = new FormData();
    formData.append("user_id", userId.value);
    formData.append("name", newName.value);
    try {
      const response = await axios.post(
        `${apiBase}/api/changeUser/`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      if (response.status === 200) {
        userName.value = newName.value;
      }
    } catch (error) {
      console.error("Ошибка при изменении имени:", error);
    }
  }
  isEdit.value = false;
  buttonAction.value = changeBtn;
  buttonText.value = "Изменить имя";
};

const fetchProducts = async () => {
  try {
    const response = await axios.get(`${apiBase}/api/getProductsById/`, {
      params: {
        userId: userId.value,
        start: 0,
        end: 10,
      },
    });

    products.value = response.data;
    products.value.forEach((product) => {
      productStatuses.value[product.id] = product.status;
    });
  } catch (error) {
    console.error("Ошибка при получении продуктов:", error);
  }
};

const updateStatus = async (product) => {
  try {
    const newStatus = productStatuses.value[product.id];
    await axios.post(`${apiBase}/api/editStatus/`, {
      product_id: product.id,
      status_id: newStatus,
    });
  } catch (error) {
    console.error("Ошибка при обновлении статуса:", error);
  }
};

const statusClass = (product) => {
  const status = productStatuses.value[product.id];
  if (status === 1) {
    return "actual-text";
  } else if (status === 2) {
    return "order-text";
  } else {
    return "sell-text";
  }
};

onMounted(() => {
  fetchUserData();
  fetchStatuses();
});
</script>

<template>
  <div class="container">
    <loading v-if="isLoading"></loading>
    <div v-else class="userInfo">
      <div class="flex justify-center items-center">
        <div class="userImage" @click="() => $refs.fileInput.click()">
          <img
            v-if="userPhoto"
            :src="userPhoto"
            alt="Фото пользователя"
            class="profile-image"
          />
          <div v-else class="placeholder">Добавить фото</div>
          <input
            type="file"
            accept="image/*"
            style="display: none"
            ref="fileInput"
            @change="handleImageUpload"
          />
        </div>

        <div class="ml-10">
          <input v-if="isEdit" v-model="newName" :placeholder="userName" />
          <h2 v-else>{{ userName }}</h2>
          <h2>{{ userEmail }}</h2>
          <sub class="help-text">*Фотографию можно изменить, нажав на нее</sub>
        </div>

        <div class="flex btns">
          <button class="btn" @click="buttonAction">
            {{ buttonText }}
          </button>
          <button class="btn exit" @click="handleLogout">Выйти</button>
        </div>
      </div>
    </div>
    <div class="products-grid">
      <div v-for="product in products" :key="product.id" class="product-item">
        <img :src="product.picture.photoPath" alt="Product Image" />
        <div class="product-info">
          <p class="card-title">{{ product.title }}</p>
          <p class="card-cost">{{ product.cost }} руб.</p>
          <select
            id="status"
            :class="statusClass(product)"
            v-model="productStatuses[product.id]"
            @change="updateStatus(product)"
            required
          >
            <option v-for="stat in statuses" :value="stat.id">
              {{ stat.title }}
            </option>
          </select>
          <a class="edit-button" :href="`/editProduct/${product.id}`">
            <img :src="editIcon" alt="Favorite" />
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "~/assets/scss/main.scss" as main;
@use "sass:color";

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 2%;

  @media (max-width: 768px) {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
}

.help-text {
  opacity: 0.5;
}

.actual-text {
  color: main.$primary-color;
}

.order-text {
  color: brown;
}

.sell-text {
  color: red;
}

.product-item {
  position: relative;
  border-radius: 5px;

  &:hover {
    transform: scale(1.02);
  }

  img {
    width: 100%;
    height: 200px;
    border-radius: 5px 5px 0 0;
    object-fit: cover;

    @media (max-width: 768px) {
      height: 150px;
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
        font-size: 14px;
      }
    }

    .card-cost {
      font-size: 18px;
      color: main.$second-color;
      letter-spacing: 1px;
      font-weight: bold;

      @media (max-width: 768px) {
        font-size: 14px;
      }
    }
  }

  .edit-button {
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

  select {
    border-radius: 15px;
    border: 2px solid main.$second-color;
    background-color: main.$window-color;
    width: 100%;
    font-weight: bold;

    &:focus {
      outline: none;
      border-color: #007bff;
      box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
    }

    option {
      font-weight: bold;
      color: black !important;
    }
  }
}

.center {
  text-align: center;
}

.userInfo {
  width: 100%;
  border-radius: 5px;
  height: max-content;
  position: relative;
  display: flex;
  align-items: center;
  padding: 1%;
  gap: 20px;
}

.userImage {
  width: 260px;
  height: 28vh;
  border-radius: 5%;
  overflow: hidden;
  cursor: pointer;
  background-color: #ccc;
  display: flex;
  align-items: center;
  justify-content: center;
}

.profile-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder {
  font-size: 14px;
  color: #666;
}

.btns {
  position: absolute;
  width: 200px;
  right: 2%;
  top: 5%;

  * {
    margin-right: 1%;
  }
}

.exit {
  background-color: rgba(255, 0, 0, 0.651) !important;
  &:hover {
    background-color: rgb(255, 0, 0);
  }
}

.btn {
  width: max-content;
  height: 4vh;
  background-color: main.$second-color;
  transition: all 1s;

  &:hover {
    transform: scale(0.95);
  }
}

h2 {
  font-size: 24px;
}
</style>
