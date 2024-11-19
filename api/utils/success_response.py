from rest_framework.response import Response


def rest_success_response(data=None, status=200):
    return Response(
        {"success": True, "data": data if data is not None else {}}, status=status
    )
