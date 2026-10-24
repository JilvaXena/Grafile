from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FileViewSet

# Default DRF Router generates CRUD
router = DefaultRouter()
router.register(r'files', FileViewSet, basename='file')

urlpatterns = [
    path('auto/', include(router.urls))
]