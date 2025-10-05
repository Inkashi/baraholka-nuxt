import { jwtDecode } from "jwt-decode";
import { useCookie, useRoute, navigateTo } from "#app";

// ~/middleware/log-visit.ts
export default defineNuxtRouteMiddleware((to, from) => {
  // Получаем ID пользователя (если авторизован через useAuth или Pinia)
  const authCookie = useCookie<string | null>("auth_token").value;
  if (authCookie != null) {
    const decodedToken: any = jwtDecode(authCookie!);
    const userId = decodedToken.user_id || null;

    // Формируем сообщение
    const logText = `Пользователь ${userId} посетил страницу ${to.fullPath}`;

    // Отправляем на бэкенд (ваш Django API)
    const config = useRuntimeConfig();
    const apiBase = config.public.apiBase;
    
    // Используем $fetch (встроенный в Nuxt)
    if (userId != null) {
      $fetch(`${apiBase}/api/log/`, {
        method: 'POST',
        body: { 'logText': logText , 'userId': userId},
        headers: {
          'Content-Type': 'application/json',
        },
        // Не ждём ответа — fire-and-forget
        async: true,
      }).catch(err => {
        // Опционально: логируем ошибку в консоль (только в dev)
        if (process.dev) {
          console.warn('Не удалось отправить лог:', err);
        }
      });
    }
  }

});