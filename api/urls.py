from django.urls import path
from api.views import index_api

urlpatterns = [
    path('index/',index_api),
]