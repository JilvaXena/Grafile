from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FileViewSet, FileAPI

# Default DRF Router generates CRUD
router = DefaultRouter()
router.register(r'files', FileViewSet, basename='file')

urlpatterns = [
    path('auto/', include(router.urls)),
    path('api/files/', FileAPI.as_view(), name='file-create'),
    path('api/files/<uuid:file_id>/', FileAPI.as_view(), name='file-detail')
]