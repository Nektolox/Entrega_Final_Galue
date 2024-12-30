# accounts/views.py

from django.urls import reverse_lazy
from django.views.generic.edit import View
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import CustomUser, TechnicalUser, CommercialUser
from django.views.generic import TemplateView

# accounts/views.py

class RegisterView(View):
    template_name = 'accounts/Register.html'
    success_url = reverse_lazy('Login')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, self.template_name, {'error': 'Las contraseñas no coinciden.'})

        if not (email.endswith('@ngtelecom.noc') or email.endswith('@ngtelecom.sales')):
            return render(request, self.template_name, {'error': 'El correo electrónico debe pertenecer a los dominios empresariales'})

        if email.endswith('@ngtelecom.noc'):
            user = TechnicalUser(username=username, email=email, first_name=first_name, last_name=last_name, password=make_password(password1))
        elif email.endswith('@ngtelecom.sales'):
            user = CommercialUser(username=username, email=email, first_name=first_name, last_name=last_name, password=make_password(password1))

        user.save()
        return redirect(self.success_url)



class HelloView(TemplateView):
    template_name = 'accounts/Login.html'
