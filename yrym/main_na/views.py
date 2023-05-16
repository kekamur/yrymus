from django.shortcuts import render,redirect
from django.http import  HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import *
from django import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def index(request):
    return render(request,'main_na/main_na.html')

@decorators.login_required
def profile_view(request):
    return render(request,'web/profile.html')


class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("profile")
    def form_valid(self,form):
        form.save()
        return super().form_valid(form)
