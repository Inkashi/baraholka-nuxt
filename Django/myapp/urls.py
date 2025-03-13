from django.urls import path
from .views import RegisterView, LoginView, LogoutView, createProduct, getCategories, getProducts, getProductsById, getUser
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('createProduct/', createProduct.as_view(), name='createProduct'),
    path('getCategories/', getCategories.as_view(), name='getCategories'),
    path('getProducts/', getProducts.as_view(), name='getProducts'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('getUser/', getUser.as_view(), name='getUserbyToken'),
    path('getProductsById/', getProductsById.as_view(), name='getProductsById')
]