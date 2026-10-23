from os import getenv
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from fileManager.models import *

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def server_info(request):
    """Check info about server for authenticated users."""
    data = {
        "banner": getenv("BANNER"),
        "version": getenv("SERVER_VERSION")
    }
    return Response(data)