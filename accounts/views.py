# accounts/views.py

from django.urls import reverse_lazy
from django.views.generic.edit import View, DeleteView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from .models import CustomUser, TechnicalUser, CommercialUser
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from accounts.decorators import technical_required, commercial_required, technical_or_commercial_or_superuser_required, superuser_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch') 
@method_decorator(technical_required, name='dispatch')
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


class CustomLoginView(LoginView):
    template_name = 'accounts/Login.html'
    
    def get_success_url(self):
        user = self.request.user
        if user.is_technical:
            return reverse_lazy('Inicio')  # Cambia 'technical_dashboard' por la URL de tu vista técnica
        elif user.is_commercial:
            return reverse_lazy('Inicio')  # Cambia 'commercial_dashboard' por la URL de tu vista comercial
        else:
            return reverse_lazy('Login')
    
    def form_invalid(self, form):
        form.add_error(None, 'Nombre de usuario o contraseña incorrectos.')
        return super().form_invalid(form)

@method_decorator(login_required, name='dispatch') 
class CustomLogoutView(LogoutView):
    template_name = 'accounts/Logout.html'
    
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        response = super().dispatch(request, *args, **kwargs)
        response.set_cookie('first_name', user.first_name)
        response.set_cookie('last_name', user.last_name)
        return response

    def get_next_page(self):
        next_page = super().get_next_page()
        if next_page:
            return next_page
        return redirect('Login')

@method_decorator(login_required, name='dispatch')  
class CustomPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'accounts/PasswordChange.html'
    success_url = reverse_lazy('change_password')
    success_message = "Tu contraseña ha sido cambiada exitosamente."


@method_decorator(login_required, name='dispatch')  
def change_avatar(request):
    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        if avatar:
            user = request.user
            if user.avatar:
                user.avatar.delete(save=False)  # Eliminar el avatar anterior
            user.avatar = avatar
            user.save()
            return redirect('Inicio')
    return render(request, 'accounts/Avatarchange.html', {'user': request.user})


@login_required 
@superuser_required
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'accounts/ListUsers.html', {'users': users})

@method_decorator(login_required, name='dispatch')  
@method_decorator(superuser_required, name='dispatch')
class UserDeleteView(UserPassesTestMixin, DeleteView):
    model = CustomUser
    template_name = 'accounts/DeleteUserCom.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return self.request.user.is_superuser

@method_decorator(login_required, name='dispatch')  
@method_decorator(superuser_required, name='dispatch')
class UserUpdateView(UserPassesTestMixin, UpdateView):
    model = CustomUser
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'accounts/UpdateUsers.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return self.request.user.is_superuser


