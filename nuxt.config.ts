// https://nuxt.com/docs/api/configuration/nuxt-config
import type { NuxtPage } from "nuxt/schema";
export default defineNuxtConfig({
  css: ["~/assets/scss/main.scss"],
  app: {
    head: {
      meta: [
        { name: "viewport", content: "width=device-width, initial-scale=1.0" },
      ],
    },
  },
  compatibilityDate: "2024-11-01",
  devtools: { enabled: true },
  modules: [
    "@nuxtjs/tailwindcss",
    "@nuxt/icon",
    "nuxt-auth-utils",
    "@pinia/nuxt",
    "pinia-plugin-persistedstate/nuxt",
  ],
  icon: {
    serverBundle: {
      collections: ["mdi"],
    },
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.API_URL || "http://localhost:8000",
    },
  },
  hooks: {
    "pages:extend"(pages) {
      function setMiddleware(pages: NuxtPage[]) {
        for (const page of pages) {
          // Добавляем глобальный middleware "auth" для всех страниц
          if (true) {
            page.meta ||= {};
            page.meta.middleware = ["auth", "log-visit"];
          }

          // Рекурсивно обрабатываем дочерние страницы
          if (page.children) {
            setMiddleware(page.children);
          }

          // Добавляем локальный middleware "edit" для конкретной страницы
          if (page.name === "editProduct-product_id") {
            page.meta.middleware = ["edit", "log-visit"];
          }
        }
      }

      // Запускаем функцию для всех страниц
      setMiddleware(pages);
    },
  },
});
