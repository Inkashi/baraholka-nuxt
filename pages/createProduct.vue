<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

const config = useRuntimeConfig();

const userId = ref();
const isLoading = ref(true);
const title = ref("");
const description = ref("");
const category = ref<number | null>(null);
const cost = ref<number | null>(null);
const picture = ref<File | null>(null); // Хранит выбранный файл
const picturePreview = ref<string | null>(null); // Хранит URL для предпросмотра
const categories = ref([]);
const apiBase = config.public.apiBase as string;

const fetchUserData = async () => {
  try {
    const token = useCookie<string | null>("auth_token").value;
    const decodedToken: any = jwtDecode(token!);

    userId.value = decodedToken.user_id || null;
  } catch (error) {
    console.error("Ошибка при получении данных пользователя:", error);
  } finally {
    isLoading.value = false;
  }
};

const fetchCategories = async () => {
  try {
    const response = await axios.get(`${apiBase}/api/getCategories/`);
    categories.value = response.data;
  } catch (error) {
    console.error("Ошибка при получении категорий:", error);
  }
};

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    const file = target.files[0];

    // Создаем временный URL для предпросмотра
    picturePreview.value = URL.createObjectURL(file);
    picture.value = file; // Сохраняем файл для отправки на сервер
  }
};

const createProduct = async () => {
  if (!picture.value) {
    alert("Пожалуйста, выберите фотографию товара.");
    return;
  }

  const formData = new FormData();
  formData.append("name", title.value);
  formData.append("description", description.value);
  formData.append("category", String(category.value));
  formData.append("seller", String(userId.value));
  formData.append("cost", String(cost.value));
  formData.append("picture", picture.value);

  try {
    const response = await axios.post(
      `${apiBase}/api/createProduct/`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    if (response.status === 200) {
      alert("Товар успешно создан!");
      title.value = "";
      description.value = "";
      category.value = null;
      cost.value = null;
      picture.value = null;
      picturePreview.value = null; // Очищаем предпросмотр
    }
  } catch (error) {
    console.error("Ошибка при создании товара:", error);
    alert("Произошла ошибка при создании товара.");
  }
};

onMounted(() => {
  fetchUserData();
  fetchCategories();
});
</script>

<template>
  <div v-if="isLoading" class="loading">
    <div class="spinner"></div>
    <p>Загрузка...</p>
  </div>

  <div v-else class="create-product-form">
    <h2>Создание карточки товара</h2>

    <form @submit.prevent="createProduct" enctype="multipart/form-data">
      <div class="form-group">
        <label for="product-photo">Загрузите фото товара</label>
        <input
          type="file"
          id="product-photo"
          ref="fileInput"
          @change="onFileChange"
        />
      </div>

      <!-- Отображение выбранной картинки -->
      <div v-if="picturePreview" class="image-preview">
        <h3>Предварительный просмотр:</h3>
        <img :src="picturePreview" alt="Превью товара" />
      </div>

      <div class="form-group">
        <label for="title">Наименование</label>
        <input type="text" id="title" v-model="title" required />
      </div>

      <div class="form-group">
        <label for="category">Категория</label>
        <select id="category" v-model="category" required>
          <option v-for="cat in categories" :value="cat.id">
            {{ cat.title }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="description">Описание</label>
        <textarea id="description" v-model="description" required></textarea>
      </div>

      <div class="form-group">
        <label for="cost">Цена</label>
        <input type="number" id="cost" v-model="cost" required />
      </div>

      <button type="submit">Создать товар</button>
    </form>
  </div>
</template>

<style scoped>
.image-preview img {
  max-width: 100%;
  height: auto;
  margin-top: 10px;
  border: 1px solid #ccc;
  padding: 5px;
}
</style>

<style scoped>
.create-product-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="file"],
input[type="text"],
input[type="number"],
textarea,
select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
