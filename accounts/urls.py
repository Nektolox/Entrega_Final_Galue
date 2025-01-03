# accounts/urls.py
from django.urls import path
from .views import RegisterView, CustomLoginView, CustomLogoutView,CustomPasswordChangeView, user_list, UserDeleteView, UserUpdateView, change_avatar



urlpatterns = [
    path('Login/', CustomLoginView.as_view(), name='Login'),
    path('Register/', RegisterView.as_view(), name='Register'),
    path('Logout/', CustomLogoutView.as_view(), name='Logout'),
    path('PasswordChange/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('Users/', user_list, name='user_list'),
    path('Users/Delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('Users/Update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('AvatarChange/', change_avatar, name='change_avatar'),
]



