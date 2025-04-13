import json

import requests
from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class TestContentView(APIView):
    
    def get(self, request, *args, **kwargs):
        return Response("OK", status=status.HTTP_201_CREATED)
