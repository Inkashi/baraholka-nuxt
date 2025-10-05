// middleware/auth.ts
import { useRuntimeConfig, useCookie, navigateTo } from "#imports";

interface TokenRefreshResponse {
  access: string;
  refresh: string;
}

// middleware/auth.ts
export default defineNuxtRouteMiddleware(async (to) => {
  if (["/auth/login", "/auth/register"].includes(to.path)) {
    return;
  }

  const { public: { apiBase } } = useRuntimeConfig();
  const authCookie = useCookie<string | null>("auth_token", {
    path: "/",
    sameSite: "lax",
  });
  const refreshCookie = useCookie<string | null>("refresh_token", {
    path: "/",
    sameSite: "lax",
  });

  // Если нет кук — редирект
  if (!authCookie.value && !refreshCookie.value) {
    return navigateTo("/auth/login");
  }

  try {
  if (!authCookie.value) {
    throw new Error('No auth token');
  }

  await $fetch(`${apiBase}/api/token/verify/`, {
    method: "POST",
    body: { token: authCookie.value },
  });
} catch (error) {
  console.error('Token failed:', error);
  // Попытка обновить токен только если есть refresh-токен
  if (!refreshCookie.value) {
    authCookie.value = null;
    refreshCookie.value = null;
    return navigateTo("/auth/login");
  }

  try {
    const response = await $fetch<TokenRefreshResponse>(
      `${apiBase}/api/token/refresh/`,
      {
        method: "POST",
        body: { refresh: refreshCookie.value },
      }
    );
    authCookie.value = response.access;
  } catch (refreshError) {
    console.error('Token refresh failed:', refreshError);
    
  }
}
});
