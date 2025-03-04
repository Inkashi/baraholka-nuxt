// https://nuxt.com/docs/api/configuration/nuxt-config
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
  modules: ["@nuxtjs/tailwindcss", "@nuxt/icon"],
  icon: {
    serverBundle: {
      collections: ["mdi"],
    },
  },
});
