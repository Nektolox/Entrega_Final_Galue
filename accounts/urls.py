# accounts/urls.py
from django.urls import path
from .views import RegisterView, CustomLoginView, CustomLogoutView,CustomPasswordChangeView, user_list, UserDeleteView, UserUpdateView



urlpatterns = [
    path('Login/', CustomLoginView.as_view(), name='Login'),
    path('Register/', RegisterView.as_view(), name='Register'),
    path('Logout/', CustomLogoutView.as_view(), name='Logout'),
    path('PasswordChange/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('users/', user_list, name='user_list'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),


]


