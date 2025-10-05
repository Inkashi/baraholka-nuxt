<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

const config = useRuntimeConfig();

const userId = ref();
const isLoading = ref(true);
const title = ref("");
const description = ref("");
const category = ref<number | null>(null);
const cost = ref<number | null>(null);
const picture = ref<File | null>(null);
const picturePreview = ref<string | null>(null);
const categories = ref([]);
const apiBase = config.public.apiBase as string;

const allFieldsFilled = computed(() => {
  return (
    !!title.value.trim() &&
    !!description.value.trim() &&
    category.value !== null &&
    cost.value !== null &&
    cost.value > 0 &&
    picture.value !== null
  );
});

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

const fileInput = ref(null);

const triggerFileInput = () => {
  fileInput.value.click();
};

const fetchCategories = async () => {
  try {
    const response = await axios.get(`${apiBase}/api/getCategories/`);
    categories.value = response.data;
    console.log(response.data);
  } catch (error) {
    console.error("Ошибка при получении категорий:", error);
  }
};

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    const file = target.files[0];

    picturePreview.value = URL.createObjectURL(file);
    picture.value = file;
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
      const logText = `Создал объявление name:${title.value}, description:${description.value}, category:${category.value},
       cost:${cost.value}`;
      await axios.post(`${apiBase}/api/log/`, {
        logText: logText,
        userId: userId.value,
        type: 2
      });
      navigateTo("/account");
      title.value = "";
      description.value = "";
      category.value = null;
      cost.value = null;
      picture.value = null;
      picturePreview.value = null;
    }
  } catch (error) {
    const logText = `Ошибка!!! Создал объявление name:${title.value}, description:${description.value}, category:${category.value},
       cost:${cost.value}`;
      await axios.post(`${apiBase}/api/log/`, {
        logText: logText,
        userId: userId.value,
        type: 2
      });
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
  <div class="container">
    <loading v-if="isLoading"></loading>

    <div v-else class="relative cont">
      <h2>Создание карточки товара</h2>

      <form @submit.prevent="createProduct" enctype="multipart/form-data" class="flex flex-row">
        <div class="form-image">
          <div class="image-alt" @click="triggerFileInput">
            <img v-if="picturePreview" :src="picturePreview" alt="Превью товара" />
            <span v-else>Загрузите <br />фото <br />товара</span>
          </div>
          <input type="file" id="product-photo" style="display: none" ref="fileInput" @change="onFileChange" />
        </div>
        <div class="form-info">
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

          <div class="form-group">
            <button class="btn" type="submit" v-if="allFieldsFilled">
              Создать
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "~/assets/scss/main.scss" as main;

.container {
  height: 60vh;
  padding: 1rem;

  @media (max-width: 768px) {
    height: auto;
    padding: 0.5rem;
  }
}

h2 {
  text-transform: uppercase;
  font-weight: bold;
  color: main.$primary-color;
  font-size: 24px;

  @media (max-width: 768px) {
    font-size: 20px;
    text-align: center;
  }
}

.form-group {
  display: flex;
  flex-direction: row;
  margin-bottom: 15px;

  @media (max-width: 1200px) {
    flex-direction: column;
    margin-left: 5%;

    textarea,
    input,
    select {
      font-size: 16px;
      width: 100%;
    }

    label {
      padding-left: 0;
    }
  }
}

label {
  width: 30%;
  font-size: 20px;
  font-weight: bold;
  color: main.$primary-color;
  padding-left: 5%;
  text-transform: uppercase;

  @media (max-width: 768px) {
    width: 100%;
    margin-bottom: 0.5rem;
  }
}

input,
textarea,
select {
  width: 70%;
  padding: 1%;
  border-radius: 15px;
  border-color: main.$primary-color;

  @media (max-width: 768px) {
    width: 100%;
    font-size: 16px;
    padding: 2%;
  }
}

input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

textarea {
  height: 120px;
  border: 2px solid #008d49;
  resize: none;
  background-color: main.$window-color;

  &:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
  }

  @media (max-width: 768px) {
    height: 100px;
  }
}

select {
  border: 2px solid main.$primary-color;
  background-color: main.$window-color;

  &:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
  }
}

.cont {
  height: 70%;

  @media (max-width: 768px) {
    height: auto;
  }
}

.btn {
  margin-left: 10px;
  margin-right: 0;
  font-size: 20px;
  padding: 0.5rem 1rem;

  @media (max-width: 768px) {
    position: relative;
    width: 100%;
    margin-top: 1rem;
  }
}

.form-image,
.form-info {
  height: 100%;

  @media (max-width: 768px) {
    width: 100% !important;
    height: auto;
  }
}

.form-info {
  width: 80%;

  @media (max-width: 768px) {
    width: 100%;
  }
}

.image-alt {
  cursor: pointer;
  text-transform: uppercase;
  font-size: 24px;
  font-weight: bold;
  color: main.$second-color;
  border: 5px solid main.$primary-color;
  border-radius: 15px;
  height: 260px;
  width: 260px;
  background-color: main.$window-color;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;

  @media (max-width: 768px) {
    width: 100%;
    max-width: 300px;
    height: 200px;
    margin: 0 auto;
    font-size: 18px;
  }

  img {
    width: 100%;
    height: 100%;
    padding: 0;
    margin: 0;
    border-radius: 10px;
    object-fit: cover;
  }
}

@media (max-width: 768px) {
  form {
    display: flex;
    flex-direction: column;
    width: 80%;
    margin-left: auto;
    margin-right: auto;
  }
}
</style>
