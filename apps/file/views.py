from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.permissions import AllowAny

from api.utils.success_response import rest_success_response
from auth_api.views import CsrfExemptSessionAuthentication
from .serializers import FileUploadSerializer


class FileUploadView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data["file"]

            file_path = default_storage.save(
                f"uploads/{file.name}", ContentFile(file.read())
            )

            return rest_success_response({"url": file_path, "key": file.name})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
