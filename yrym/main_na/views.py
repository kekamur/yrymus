from django.shortcuts import render,redirect
from .forms import ProfileUpdateForm, UserUpdateForm,Profile,PostsForm
from django.http import  HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import *
from django import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import DetailView, ListView
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from .models import Posts
from django.db.models import Q
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


# Create your views here.
def index(request):
    feed = Posts.objects.order_by('-date')[:10]
    return render(request,'main_na/main_na.html', {'feed':feed} )

@decorators.login_required
def profile_view(request):
    feed = Posts.objects.order_by('-date')[:10]
    return render(request,'web/profile.html', {'feed':feed} )

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'web/profile_detail_view.html'
    context_object_name = 'detailprofile'
    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = Posts.objects.order_by('-date')
        context = super().get_context_data(**kwargs)
        context['feed'] = object_list
        return context

@decorators.login_required
def new(request):
    error = ''
    if request.method=='POST':
        form = PostsForm(request.POST, request.FILES)

        if form.is_valid():
            form=form.save(commit=False)
            form.author=request.user
            form.save()
            return redirect('home')
        else:
            error = 'Форма заполнена неправильно'
    form = PostsForm()
    data = {
        'form': form,
        'error': error,
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

class SearchResultsView(ListView):
    template_name = 'main_na/search_results.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Posts.objects.filter(
            Q(title__icontains=query) | Q(author__username__icontains=query)
        )
        return object_list[:20]
    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = self.request.GET.get('q')
        context = super().get_context_data(**kwargs)
        context['query'] = object_list
        return context


def about(request):
    return render(request,'main_na/about.html')