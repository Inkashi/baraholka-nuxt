<script setup lang="ts">
import axios from "axios";
import { ref, onMounted } from "vue";
import { jwtDecode } from "jwt-decode";

const isLoading = ref(true);
const config = useRuntimeConfig();
const apiBase = config.public.apiBase as string;
const stats = ref();
const userId = ref();
const userCount = ref('');


const fetchUserData = async () => {
    try {
        const response = await axios.post(`${apiBase}/api/getStatsLogs/`);
        stats.value = response.data;
        console.log(stats.value);
    } catch (error) {
        console.error("Ошибка при получении данных:", error);
    } finally {
        isLoading.value = false;
    }
};

const getUserCountLogs = async () => {
    try {
        const response = await axios.post(`${apiBase}/api/countRegisterToChat/`, {'userId':userId.value});
        userCount.value = response.data;
        console.log(userCount.value);
    } catch (error) {
        console.error("Ошибка при получении данных:", error);
    }
};

onMounted(() => {
    fetchUserData();
});

</script>

<template>
  <loading v-if="isLoading"></loading>
  <div v-else class="container">
    <div class="stats-grid">
      <!-- 1. Блок ввода и счётчика -->
      <div class="stat-card">
        <input type="text" @change="getUserCountLogs" v-model="userId" placeholder="ID пользователя" />
        <h2>Количество действий пользователя<br>регистрация → чат</h2>
        <p class="result">{{ userCount }}</p>
      </div>

      <!-- 2. Регистрации / Авторизации -->
      <div class="stat-card">
        <h2>Активность пользователей</h2>
        <p>Зарегистрировано — {{ stats.lr[1] }}</p>
        <p>Авторизировано — {{ stats.lr[0] }}</p>
      </div>

      <!-- 3. Смена статуса объявлений -->
      <div class="stat-card">
        <h2>Смена статуса объявления на</h2>
        <p>Актуально — {{ stats.statuses[0] }}</p>
        <p>Забронировано — {{ stats.statuses[1] }}</p>
        <p>Продано — {{ stats.statuses[2] }}</p>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "~/assets/scss/main.scss" as main;
@use "sass:color";

.container {
  padding: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin: 0 auto;
  max-width: 1200px;

  @media (max-width: 900px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 600px) {
    grid-template-columns: 1fr;
  }
}

.stat-card {
  background-color: rgba(255, 255, 255, 0.075);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  text-align: center

  h2 {
    font-size: 1.2rem;
    margin-bottom: 16px;
    font-weight: 600;
  }

  p {
    margin: 8px 0;
    font-size: 1rem;
  }

  input {
    width: 100%;
    padding: 8px 12px;
    margin-bottom: 16px;
    border-radius: 6px;
    border: 1px solid #ccc;
    background: rgba(0, 0, 0, 0.2);
    color: white;
    box-sizing: border-box;

    &::placeholder {
      color: #aaa;
    }
  }

  .result {
    font-size: 1.4rem;
    font-weight: bold;
    color: #4ade80; /* красивый акцентный цвет */
    margin-top: 10px;
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
        transition: all 0.3s ease;

        &:hover {
            color: rgb(182, 182, 182);
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
        background-color: color.scale(main.$window-color,
                $lightness: +15%,
                $alpha: -10%);
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
                background-color: #ffffff;
            }
        }
    }
}

.table {
    display: grid;
    background-color: rgba(201, 201, 201, 0.534);
    width: 70%;
    margin-left: auto;
    margin-right: auto;
    border-radius: 15px;
    border: 2px solid rgba(141, 141, 141, 0.658);
    // grid-template-rows: 1fr;
    grid-column: 1;
}

.row {
    display: grid;
    margin-top: 5px;
    grid-template-columns: 1fr 3fr 1fr;
}

.id {
    margin-left: 30%;
    // margin-right: 8%;
}

.idH {
    margin-left: 17%;
    font-weight: bold;
}

.textH {
    width: 80%;
    text-align: center;
    font-weight: bold;
}

.timeH {
    margin-left: 8%;
    font-weight: bold;
}

.text {
    margin-right: 5%;
    text-align: left;
}

.timestamp {
    // margin-right: 5%;
    text-align: left;
}

.button {
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
    transition: all 0.3s ease;

    &:hover {
        color: rgb(182, 182, 182);
    }

    .icon {
        margin-left: 10px;
        font-size: 12px;
    }
}

.navigator-buttons {
    margin-top: 10px;
    display: flex;
    justify-content: center;
    gap: 7px;
}
</style>