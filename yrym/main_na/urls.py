from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from . import views
urlpatterns = [
    path('',views.index,name='home'),
    path('profile',views.profile_view,name='profile'),
    path('register',views.RegisterView.as_view(),name='register'),
    path('edit-profile', views.ProfileEditView.as_view(), name='profile-edit'),
    path('new',views.new,name='new'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
