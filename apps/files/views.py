from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from models import File

from .serializers import FileSerializer

@require_http_methods(["GET"])
def search_api(request):
    file_id = request.GET.get('file_id')
    file_name = request.GET.get('file_name')

    if file_id:
        files_queryset = File.objects.filter(file_id=file_id).all()
    elif file_name:
        files_queryset = File.objects.filter(file_name=file_name).all()
        

class FileViewSet(viewsets.ViewSet):
    """
    Set user id automatically.
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Assign user
        serializer.save(user_created=self.request.user)