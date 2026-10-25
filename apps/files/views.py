from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from models import File

from .serializers import FileSerializer

@require_http_methods(["GET"])
def search_file(request):
    file_id = request.GET.get('file_id')
    file_name = request.GET.get('file_name')

    if file_id:
        files_queryset = File.objects.filter(file_id=file_id).all()
    elif file_name:
        files_queryset = File.objects.filter(file_name__icontains=file_name).all()
    else:
        return JsonResponse({"error": "Either file id or file name needed to perform the search"}, status=400)
    
    results = list(files_queryset.values('file_id', 'file_name', 'group'))
    return JsonResponse({"results": results}, safe=False)

@require_http_methods(["POST", "PUT"])
class file_api(request):
    """Handling of updating and adding new files."""
    if request.method == "POST":
        # New File
        file_name = request.POST.get("file_name")
        file_algorithm = request.POST.get("file_algorithm")
        file_group = request.POST.get("file_group")
        file_content = request.FILE.get("file_content")

        #TODO: missing argument and group handling
        if not file_algorithm or not file_algorithm or not file_content:
            pass
        if file_group:
            pass

        file = File.objects.create(
            file_name=file_name,
            file_algorithm=file_algorithm,
            group=file_group,
            file=file
        )

    #TODO: update file and error handling
    elif request.method == "PUT":
        # Update file
        pass
    else:
        # Error
        pass

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