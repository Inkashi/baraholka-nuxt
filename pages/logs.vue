<script setup lang="ts">
import axios from "axios";
import { ref, onMounted } from "vue";
import { jwtDecode } from "jwt-decode";

const isLoading = ref(true);
const config = useRuntimeConfig();
const apiBase = config.public.apiBase as string;
const isSortDropdownOpen = ref(false);
const selectedSortOption = ref<string | null>(null);
const sortOption = ref<string>("new");
const page = ref(1);
const userID = ref("");
const logs = ref([]);
const userId = ref<number | null>(null);

const toggleSortDropdown = () => {
    isSortDropdownOpen.value = !isSortDropdownOpen.value;
};

const selectSortOption = (option: string) => {
    sortOption.value = option;
    isSortDropdownOpen.value = false;
    getSearch();
};

const getSearch = async () => {
    try {
        const formData = new FormData();
        if (sortOption.value === "Посещение страниц")
            formData.append("type", "1");
        else if (sortOption.value === "Объявление")
            formData.append("type", "2");
        else if (sortOption.value === "Чат")
            formData.append("type", "3");

        formData.append("page", String(page.value));
        if (userID.value != "") {
            formData.append("userId", String(userID.value));
        }
        // console.log
        const response = await axios.post(`${apiBase}/api/getLogs/`, formData);
        logs.value = response.data;
    } catch (error) {
        console.error("Ошибка:", error);
    }
};

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
        const formData = new FormData();
        formData.append("page", page.value);
        const response = await axios.post(`${apiBase}/api/getLogs/`, formData);
        logs.value = response.data;
    } catch (error) {
        console.error("Ошибка при получении данных:", error);
    } finally {
        isLoading.value = false;
    }
};

onMounted(() => {
    fetchUserData();
});

</script>

<template>
    <loading v-if="isLoading"></loading>
    <div v-else class="container">
        <div class="center">
            <div class="search-bar">
                <div><input type="text" placeholder="UserID" v-model="userID" @change="getSearch();"></div>
                <div class="category-selector sort-selector">
                    <button class="button" @click="toggleSortDropdown">
                        {{ selectedSortOption || "Категория" }}
                    </button>
                    <ul v-if="isSortDropdownOpen" class="category-dropdown">
                        <li @click="selectSortOption('Все')">Все</li>
                        <li @click="selectSortOption('Посещение страниц')">Посещение страниц</li>
                        <li @click="selectSortOption('Объявление')">Объявление</li>
                        <li @click="selectSortOption('Чат')">
                            Чат
                        </li>
                    </ul>
                </div>
            </div>
            <div class="table">
                <div class="row">
                    <div class="column idH">
                        <p>UserID</p>
                    </div>
                    <div class="column textH">
                        <p>Text</p>
                    </div>
                    <div class="column timeH">
                        <p>Time</p>
                    </div>
                </div>
                <div class="row" v-for="log in logs">
                    <div class="column id">
                        <p>{{ log.user_id }}</p>
                    </div>
                    <div class="column text">
                        <p>{{ log.text }}</p>
                    </div>
                    <div class="column timestamp">
                        <p>{{ log.created.slice(0, 10).replaceAll('-', '.') + ' ' + log.created.slice(11, 19) }}</p>
                    </div>
                </div>
            </div>
            <div class="navigator-buttons">
                <button class="button" :disabled="page == 1" @click="page--; getSearch();">
                    < </button>
                        <button class="button" @click="page++; getSearch();">></button>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
@use "~/assets/scss/main.scss" as main;
@use "sass:color";

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