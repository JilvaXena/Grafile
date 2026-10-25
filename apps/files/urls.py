from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FileViewSet, search_file

# Default DRF Router generates CRUD
router = DefaultRouter()
router.register(r'files', FileViewSet, basename='file')

urlpatterns = [
    path('auto/', include(router.urls)),
    path('search/file/', search_file, name='search_file')
]