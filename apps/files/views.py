from django.shortcuts import render
from django.http import FileResponse
from django.views.decorators.http import APIView
from rest_framework import viewsets, status
from rest_framweork.response import Response
from rest_framework.permissions import IsAuthenticated

from models import File, Group

from .serializers import FileSerializer
from .errors import ErrorCode


class FileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
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
            return Response(
                {"errors": errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        file = File.objects.create(
            file_name=file_name,
            file_algorithm=file_algorithm,
            group=group,
            file=file_content
        )
        return Response({
            "message": "File created successfully",
            "file_id": file.file_id
            }, status=status.HTTP_201_CREATED)


    def get(self, request, file_id=None, *args, **kwargs):
        #TODO: update file and error handling
        errors = []

        if not file_id:
            errors.append({
                "code": ErrorCode.MISSING_FIELD,
                "message": f"File ID was not provided."
            })
            return Response(
                {"errors": errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file = File.objects.filter(file_id=file_id).first()
        if not file:
            errors.append({
                "code": ErrorCode.FILE_NOT_FOUND,
                "message": ErrorCode.FILE_NOT_FOUND.label
            })
            return Response(
                {"errors": errors},
                status=status.HTTP_404_NOT_FOUND
            )
        download_param = request.query_params.get('download', 'false').lower()
        download = download_param in ['true', '1', 'yes']

        if download:
            file_contents = file.file.open('rb')
            filename = file.file.name.split('/')[-1]
            response = FileResponse(file_contents, as_attachment=True, filename=filename)

        #TODO: complete info and add size, etc.
        file_data = {
            "file_id": str(file.file_id),
            "file_name": file.file_name,
            "file_algorithm": file.file_algorithm,
            "group": file.group.group_id if file.group else None,
            "created_at": file.date_created,
            "user_created": file.user_created
        }
        return Response(
            {"file": file_data},
            status=status.HTTP_200_OK
        )

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