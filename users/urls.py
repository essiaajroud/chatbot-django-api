from django.urls import path
from . import views
from .views import save_chat_message

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('save-chat-message/', save_chat_message, name='save_chat_message'),
]
