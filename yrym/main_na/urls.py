from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .views import profile_view
from .views import RegisterView
urlpatterns = [
    path('',views.index,name='home'),
    path('profile',profile_view,name='profile'),
    path('register',RegisterView.as_view(),name='register')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
