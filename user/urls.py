from django.contrib import admin
from django.urls import path
from .views import ProfileView

urlpatterns = [
    path('profile/', ProfileView),
]