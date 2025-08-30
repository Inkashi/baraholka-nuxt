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
  } catch (error) {
    console.error("Ошибка при декодировании токена:", error);
    return navigateTo("/login");
  }

  const route = useRoute();
  const productId = route.params.product_id as string;

  try {
    // Получаем данные о продукте через API с использованием axios
    console.log(productId); // Логируем ID продукта для отладки
    const response = await axios.get(`${apiBase}/api/getProductById/`, {
      params: { product_id: productId },
    });
    console.log(response.data); // Логируем ответ API

    const product = response.data;

    // Проверяем, является ли текущий пользователь создателем продукта
    if (product.seller !== userId) {
      console.warn("У пользователя нет прав для редактирования этого продукта");
      return navigateTo("/"); // Перенаправляем на главную страницу
    }
  } catch (error) {
    console.error("Ошибка при проверке прав доступа:", error);
    return navigateTo("/"); // В случае ошибки перенаправляем на главную
  }
});
