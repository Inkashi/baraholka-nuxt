from django.urls import path
from .views import RegisterView, LoginView, LogoutView, createProduct, getCategories, getProducts

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('createProduct/', createProduct.as_view(), name='createProduct'),
    path('getCategories/', getCategories.as_view(), name='getCategories'),
    path('getProducts/', getProducts.as_view(), name='getProducts'),
]