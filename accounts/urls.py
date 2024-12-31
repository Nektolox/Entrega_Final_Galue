# accounts/urls.py
from django.urls import path
from django.urls import path
from .views import RegisterView, CustomLoginView, CustomLogoutView

urlpatterns = [
    path('Login/', CustomLoginView.as_view(), name='Login'),
    path('Register/', RegisterView.as_view(), name='Register'),
    path('Logout/', CustomLogoutView.as_view(), name='Logout'),
]


