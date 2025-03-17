from django.urls import path
from .views import RegisterView, LoginView, LogoutView, createProduct, getCategories, getProducts, getProductsById, getUser, getMessages, getChats, changeUserProfile, getUsersByChat, getChatByUsers, getFavoriteCollectionByUser, getFavorites, addFavorite, getProductById, editProduct, editStatus, getStatuses, getSearched, deleteProduct
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

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
    path('getProductsById/', getProductsById.as_view(), name='getProductsById'),
    path('getMessages/', getMessages.as_view(), name='getMessages'), 
    path('getChats/', getChats.as_view(), name='getChats'),
    path('getUsersByChat/', getUsersByChat.as_view(), name='getUsersByChat'),
    path('changeUser/', changeUserProfile.as_view(), name='changeUserProfile'),
    path('getChatByUsers/', getChatByUsers.as_view(), name='getChatByUsers'),
    path('getFavoriteCollection/', getFavoriteCollectionByUser.as_view(), name='getFavoriteCollectionByUser'),
    path('getFavorites/', getFavorites.as_view(), name='getFavorites'),
    path('addFavorite/', addFavorite.as_view(), name='addFavorite'),
    path('getProductById/', getProductById.as_view(), name='getProductById'),
    path('editProduct/', editProduct.as_view(), name='editProduct'),
    path('editStatus/', editStatus.as_view(), name='editStatus'),
    path('getStatuses/', getStatuses.as_view(), name='getStatuses'),
    path('getSearched/', getSearched.as_view(), name='getSearched'),
    path('deleteProduct/<int:product_id>/', deleteProduct.as_view(), name='deleteProduct'),
]