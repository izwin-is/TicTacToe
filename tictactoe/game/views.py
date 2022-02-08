from random import randint

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView

from game.forms import RegisterUserForm, LoginUserForm
from game.utils import *

# def index(request):
#     return HttpResponse('main')



class HomePage(DataMixin, TemplateView):
    template_name = 'game/home.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context:
            context = dict()
        context['title'] = 'Главная'
        # context['cat_selected'] = 0
        context['mainstyle'] = 'game/css/home.css'
        context['rand'] = randint(2, 5000)
        c_def = self.get_user_context()
        return {**context, **c_def}


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'game/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self,* , object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context:
            context = dict()
        context['mainstyle'] = 'game/css/register.css'
        context['rand'] = randint(2, 5000)
        c_def = self.get_user_context(title='Регистрация')
        return {**context, **c_def}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'game/register.html'\


    def get_context_data(self,* , object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context:
            context = dict()
        context['mainstyle'] = 'game/css/register.css'
        context['rand'] = randint(2, 5000)
        c_def = self.get_user_context(title='Авторизация')
        return {**context, **c_def}

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')

def play(request):
    return render(request, 'play/about.html')

def profile(request):
    return render(request, 'profile/about.html')

def liders(request):
    return render(request, 'liders/about.html')
