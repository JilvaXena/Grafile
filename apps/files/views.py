from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from django.views.decorators.http import require_http_methods, APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from models import File, Group

from .serializers import FileSerializer
from .errors import ErrorCode


class FileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(request):
        file_id = request.data.get('file_id')
        file_name = request.data.get('file_name')

        if file_id:
            files_queryset = File.objects.filter(file_id=file_id).all()
        elif file_name:
            files_queryset = File.objects.filter(file_name__icontains=file_name).all()
        else:
            return JsonResponse({"error": "Either file id or file name needed to perform the search"}, status=400)
    
        results = list(files_queryset.values('file_id', 'file_name', 'group'))
        return JsonResponse({"results": results}, safe=False)

    def post(request):
        """Handling of updating and adding new files."""
        #TODO: Check http error codes
        # New File
        file_name = request.data.get("file_name")
        file_algorithm = request.data.get("file_algorithm")
        file_group = request.data.get("file_group")
        file_content = request.FILES.get("file_content")
        group = None

        errors = []

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
        file_id = request.PUT.get("file_id")
        errors = []

        if not file_id:
            errors.append({
                "code": ErrorCode.MISSING_FIELD,
                "message": f"File ID was not provided."
            })
            return JsonResponse({"errors": errors}, status=400)
        
        file = File.objects.filter(file_id=file_id).first()
        if not file:
            errors.append({
                "code": ErrorCode.FILE_NOT_FOUND,
                "message": ErrorCode.FILE_NOT_FOUND.label
            })
            return JsonResponse({"errors": errors}, status=400)
        file_contents = file.file.open('rb')
        filename = file.file.name.split('/')[-1]
        response = FileResponse(file_contents, as_attachment=True, filename=filename)

        return response

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