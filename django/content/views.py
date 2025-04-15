from project_service.decorations import validate_jwt
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils.decorators import method_decorator


@method_decorator(validate_jwt, name='dispatch')
class ContentView(APIView):
    authentication_classes = [] 
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response("OK", status=status.HTTP_201_CREATED)
