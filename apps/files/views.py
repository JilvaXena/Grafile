from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from models import File, Group

from .serializers import FileSerializer
from .errors import ErrorCode

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
def file_api(request):
    """Handling of updating and adding new files."""
    if request.method == "POST":
        # New File
        file_name = request.POST.get("file_name")
        file_algorithm = request.POST.get("file_algorithm")
        file_group = request.POST.get("file_group")
        file_content = request.FILES.get("file_content")
        group = None

        errors = []

        #TODO: missing argument and group handling
        if not file_algorithm or not file_name or not file_content:
            if not file_algorithm:
                errors.append({
                    "code": ErrorCode.MISSING_FIELD,
                    "message": "Field file_algorithm not provided."
                })
            if not file_name:
                errors.append({
                    "code": ErrorCode.MISSING_FIELD,
                    "message": f"FIELD file_name not provided."
                })
            if not file_content:
                errors.append({
                    "code": ErrorCode.MISSING_FILE_CONTENT,
                    "message": ErrorCode.MISSING_FILE_CONTENT.label
                })
        if file_group:
            group = Group.objects.filter(group_id=file_group).first()
            if not group:
                errors.append({
                    "code": ErrorCode.GROUP_NOT_FOUND,
                    "message": f"Group {file_group} was not found."
                })
        
        if errors:
            return JsonResponse({"errors": errors}, status=400)

        file = File.objects.create(
            file_name=file_name,
            file_algorithm=file_algorithm,
            group=group,
            file=file_content
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