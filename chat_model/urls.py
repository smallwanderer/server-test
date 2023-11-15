from django.urls import path

from . import views
from .views import index_basic, index_rest, submit_text, PredictSentence

urlpatterns = [
    path("", views.ChatView.as_view(), name='chat_model'),
    path("basic/", index_basic, name='index_basic'),
    path("rest/", index_rest, name='index_rest'),
    path("basic/index-basic/", submit_text, name='submit_text1'),
    path("rest/index-rest/", PredictSentence.as_view(), name='submit_text2')
]
