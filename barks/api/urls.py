from django.contrib import admin
from django.urls import path

from .views import (
    bark_detail_view, bark_list_view, 
    bark_create_view, bark_delete_view, bark_action_view,
)

urlpatterns = [
    path('', bark_list_view),
    path('action/', bark_action_view),
    path('create/', bark_create_view),
    path('<int:bark_id>/', bark_detail_view),
    path('<int:bark_id>/delete/', bark_delete_view),
]
