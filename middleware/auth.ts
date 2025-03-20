// middleware/auth.ts
import { useRuntimeConfig, useCookie, navigateTo } from "#imports";

interface TokenRefreshResponse {
  access: string;
  refresh: string;
}

export default defineNuxtRouteMiddleware(async (to) => {
  if (["/auth/login", "/auth/register"].includes(to.path)) {
    return;
  }

  const {
    public: { apiBase },
  } = useRuntimeConfig();
  const userStore = useAuthStore();
  const authCookie = useCookie<string | null>("auth_token");
  const refreshCookie = useCookie<string | null>("refresh_token");
  if (!userStore.isAuth) {
    authCookie.value = null;
    refreshCookie.value = null;
    return redirectToMain();
  }

  if (!authCookie.value && !refreshCookie.value) {
    userStore.logoutUser();
    return redirectToMain();
  }

  try {
    await $fetch(`${apiBase}/api/token/verify/`, {
      method: "POST",
      body: { token: authCookie.value },
    });
    isAuth();
  } catch {
    try {
      const response = await $fetch<TokenRefreshResponse>(
        `${apiBase}/api/token/refresh/`,
        {
          method: "POST",
          body: { refresh: refreshCookie.value },
        }
      );
      authCookie.value = response.access;
      isAuth();
    } catch {
      authCookie.value = null;
      refreshCookie.value = null;
      userStore.logoutUser();
      return redirectToMain();
    }
  }

  function redirectToMain() {
    if (to.path !== "/") {
      return navigateTo("/", { external: true });
    }
  }

  function isAuth() {
    if (!userStore.isAuth) {
      userStore.loginUser();
    }
  }
});
