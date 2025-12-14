from rest_framework.response import Response
from rest_framework import status as drf_status

def api_response(success, message, data=None, status=200):
    print("API_RESPONSE FUNCTION CALLED") 
    return Response(
        {
            "success": success,
            "message": message,
            "data": data
        },
        status=status
    )
