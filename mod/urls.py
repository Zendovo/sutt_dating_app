from django.contrib import admin
from django.urls import path
from .views import ModView, ProfilesView

urlpatterns = [
    path('', ModView.as_view()),
    path('profiles/', ProfilesView.as_view()),
]