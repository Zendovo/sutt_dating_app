from django.contrib import admin
from django.urls import path
from .views import ModView

urlpatterns = [
    path('', ModView.as_view()),
]