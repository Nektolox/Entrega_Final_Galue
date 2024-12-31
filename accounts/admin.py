from django.contrib import admin

AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_REDIRECT_URL = 'Inicio'  # Cambia 'home' por la URL de tu página principal
LOGOUT_REDIRECT_URL = 'Logout'

