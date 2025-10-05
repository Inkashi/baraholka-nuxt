import { createPinia } from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

export const useAuthStore = defineStore("auth", {
  state: () => ({
    isAuth: false,
  }),
  actions: {
    loginUser() {
      this.isAuth = true;
      navigateTo("/");
    },
    logoutUser() {
      this.isAuth = false;
      navigateTo("/");
    },
  },
  persist: true,
});
