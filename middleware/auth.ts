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

  const config = useRuntimeConfig();
  const apiBase = config.public.apiBase as string;

  const authCookie = useCookie<string | null>("auth_token");
  const refreshCookie = useCookie<string | null>("refresh_token");

  if (to.path.startsWith("/api") || to.path.includes("._nuxt")) return;

  if (!authCookie.value || !refreshCookie.value) {
    return redirectToLogin();
  }

  try {
    await $fetch(`${apiBase}/api/token/verify/`, {
      method: "POST",
      body: { token: authCookie.value },
    });
  } catch {
    try {
      // Явно указываем тип ответа
      const response = await $fetch<TokenRefreshResponse>(
        `${apiBase}/api/token/refresh/`,
        {
          method: "POST",
          body: { refresh: refreshCookie.value },
        }
      );

      // Теперь TypeScript знает о структуре ответа
      authCookie.value = response.access;
      refreshCookie.value = response.refresh;
    } catch {
      authCookie.value = null;
      refreshCookie.value = null;
      return redirectToLogin();
    }
  }

  function redirectToLogin() {
    return navigateTo("/auth/login");
  }
});
