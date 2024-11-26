import uuid
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

            file_uuid = uuid.uuid4().hex
            file_name = f"{file_uuid[:8]}_{file.name.replace(" ", "")}"

            file_path = default_storage.save(
                f"uploads/{file_name}", ContentFile(file.read())
            )

            uploaded_file = {
                "key": file_uuid,
                "url": default_storage.url(file_path),
                "name": file_name,
            }

            return rest_success_response(uploaded_file)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
