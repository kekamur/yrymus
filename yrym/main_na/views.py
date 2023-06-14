from django.shortcuts import render,redirect
from .forms import ProfileUpdateForm, UserUpdateForm,Profile,PostsForm
from django.http import  HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import *
from django import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from .models import Posts
# Create your views here.
def index(request):
    feed = Posts.objects.order_by('-date')[:10]
    return render(request,'main_na/main_na.html', {'feed':feed} )

@decorators.login_required
def profile_view(request):
    return render(request,'web/profile.html')

def new(request):
    error = ''
    if request.method=='POST':
        form = PostsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форма заполнена неправильно'

    form = PostsForm()
    data = {
        'form': form,
        'error' : error
    }
    return render(request,'main_na/new.html',data)

class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("profile")
    def form_valid(self,form):
        form.save()
        return super().form_valid(form)

class ProfileEditView(UpdateView):
    """
    Представление для редактирования профиля пользователя.
    """
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'web/profile-edit.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(ProfileEditView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile')