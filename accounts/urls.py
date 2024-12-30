# accounts/urls.py
from django.urls import path
from django.urls import path
from .views import RegisterView, HelloView

urlpatterns = [
    path('Login/', HelloView.as_view(), name='Login'),
    path('Register/', RegisterView.as_view(), name='Register'),
]


