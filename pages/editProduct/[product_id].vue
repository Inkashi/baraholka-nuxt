<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

const config = useRuntimeConfig();

const product_id = useRoute().params.product_id
const product = ref();

const userId = ref();
const isLoading = ref(true);
const title = ref('');
const description = ref('');
const category = ref<number | null>(null);
const cost = ref<number | null>(null);
const picture = ref<File | null>(null);
const categories = ref([]);
const apiBase = config.public.apiBase as string;

const fetchUserData = async () => {
  try {
    const token = useCookie<string | null>("auth_token").value;
    const decodedToken: any = jwtDecode(token!);

    userId.value = decodedToken.user_id || null;

    fetchProductData();
  } catch (error) {
    console.error("Ошибка при получении данных пользователя:", error);
  } finally {
    isLoading.value = false;
  }};

  const fetchCategories = async () => {
    try {
        const response = await axios.get(`${apiBase}/api/getCategories/`);
        categories.value = response.data;
    } catch (error) {
        console.error("Ошибка при получении категорий:", error);
    }
};

const fetchProductData = async () => {
    try {
        const response = await axios.get(`${apiBase}/api/getProductById/`,
            {
                params: { product_id:product_id }
            }
        );
        product.value = response.data;
        title.value = product.value.title;
        cost.value = product.value.cost;
        picture.value = product.value.picture.photoPath;
        description.value = product.value.description;
        category.value = product.value.category;
    } catch (error) {
        console.error("Ошибка при получении категорий:", error);
    }
};

const onFileChange = (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files[0]) {
        picture.value = target.files[0];
    }
};

const editProduct = async () => {

    const formData = new FormData();
    formData.append('id', String(product_id));
    formData.append('name', title.value);
    formData.append('description', description.value);
    formData.append('category', String(category.value));
    formData.append('seller', String(userId.value));
    formData.append('cost', String(cost.value));
    if (picture.value)
        formData.append('picture', picture.value);

    try {
        const response = await axios.post(`${apiBase}/api/editProduct/`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });

        if (response.status === 200) {
           navigateTo('/account');
        }
    } catch (error) {
        console.error("Ошибка при создании товара:", error);
        alert('Произошла ошибка при создании товара.');
    }
};

const deleteProduct = async () => {

const formData = new FormData();
formData.append('id', String(product_id));

console.log(product_id)

try {
    const response = await axios.delete(`${apiBase}/api/deleteProduct/${product_id}/`);

    if (response.status === 200) {
       navigateTo('/account');
    }
} catch (error) {
    console.error("Ошибка при удалении товара:", error);
    alert('Ошибка при удалении товара.');
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

        <form @submit.prevent="editProduct" enctype="multipart/form-data">
            <div class="form-group">
                <label for="product-photo">Загрузите фото товара</label>
                <input type="file" id="product-photo" ref="fileInput" @change="onFileChange" />
            </div>

            <div class="form-group">
                <label for="title">Наименование</label>
                <input type="text" id="title" v-model="title" required />
            </div>

            <div class="form-group">
                <label for="category">Категория</label>
                <select id="category" v-model="category" required>
                    <option v-for="cat in categories" :value="cat.id">{{ cat.title }}</option>
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

            <button type="submit">Изменить товар</button>
            <button @click="deleteProduct">Удалить товар</button>
        </form>
    </div>
</template>

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