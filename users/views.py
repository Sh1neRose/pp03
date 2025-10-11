from django.shortcuts import render, redirect
from django.views import View
from .forms import CustomUserCreationForm, CustomUserLogin
from django.contrib.auth import login, logout

class register(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'users/register.html',{
            'form': form,
        })
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('users:register')
        
class login_view(View):
    def get(self, request):
        form = CustomUserLogin()
        return render(request, 'users/login.html',{
            'form': form,
        })
    def post(self, request):
        form = CustomUserLogin(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

class logout_view(View):
    def get(self, request):
        logout(request)
        return redirect('users:register')