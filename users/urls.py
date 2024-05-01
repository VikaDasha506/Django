from django.urls import path
from . import views

app_name = 'users'  # Пространство имен для приложения

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('signup/', views.RegisterUser.as_view(), name='signup'),
    path('thanks/', views.ThanksForRegister.as_view(), name='thanks')
]