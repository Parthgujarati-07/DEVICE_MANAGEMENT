from rest_framework.response import Response
from rest_framework import status as drf_status

def api_response(success, message, data=None, status=drf_status.HTTP_200_OK):
    return Response(
        {
            "success": success,
            "message": message,
            "data": data
        },
        status=status
    )
