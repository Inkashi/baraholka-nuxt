import { jwtDecode } from "jwt-decode";
import axios from "axios";
import { useCookie, useRoute, navigateTo } from "#app";

export default defineNuxtRouteMiddleware(async (to) => {
  const {
    public: { apiBase },
  } = useRuntimeConfig();
  const authCookie = useCookie<string | null>("auth_token").value;
  let userId: number | null = null;
  try {
    const decodedToken: any = jwtDecode(authCookie!);
    userId = decodedToken.user_id || null;
    const is_super_user = decodedToken.is_superuser || null;
    if (!is_super_user) {
    return navigateTo('/');
  }
  } catch (error) {
    console.error("Ошибка при декодировании токена:", error);
    return navigateTo("/login");
  }
});
