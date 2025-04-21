from logs.logs_util import user_log_action
from logs.models import LogAction
from project_service.decorations import validate_jwt
from project_service.utils import decrypt_id
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils.decorators import method_decorator

from ..models.address import City
from ..models.user import User
from ..serializers import UserDisplaySerializer, UserSerializer


#Only Django admin users can access
class ListUsers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# PUblic Create account API
class PublicUserCreationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(validate_jwt, name='dispatch')
class UserDetailAPIView(APIView):
    authentication_classes = [] 
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.logged_user
        serializer = UserDisplaySerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.logged_user
        city_id = request.data["city"]
        request.data["city"] = decrypt_id(city_id, City._meta.db_table)
        
        serializer = UserSerializer(user, data=request.data)
        user_log_action(
                    user=user,
                    action=LogAction.USER_DATA_UPDATE)
        
        if serializer.is_valid():
            serializer.save()
            return Response("OK", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


