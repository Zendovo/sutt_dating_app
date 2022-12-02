from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='chat_index'),
    path('<int:chat_id>/', views.ChatRoom.as_view(), name='chat_room')
]
