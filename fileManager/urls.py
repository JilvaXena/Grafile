from django.urls import path
from .views import server_info

urlpatterns = [
    path('info', server_info, name='server_info'),
]