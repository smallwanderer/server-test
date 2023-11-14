from django.urls import path

from . import views
from .views import index

urlpatterns = [
    path("", views.ChatView.as_view(), name='chat_model'),
    path("test/", index, name='idnex'),
]
