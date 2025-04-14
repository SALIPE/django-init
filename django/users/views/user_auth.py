import jwt
from rest_framework.views import APIView

from django.conf import settings
from django.http import JsonResponse

from ..models.user import User
from ..serializers import UserAuthTokenSerializer
from ..utils import generate_jwt_token

JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = "HS256"

class UserObtainTokenPairView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = UserAuthTokenSerializer(data=request.data)
       
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token = generate_jwt_token(user)
        return JsonResponse({"token": token})
    
    
class UserRefreshTokenView(APIView):
    def post(self, request, *args, **kwargs):
        
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({"error": "No refresh token provided"}, status=400)

        refresh_token = auth_header.split(" ")[1]
        if not refresh_token:
            return JsonResponse({"error": "No refresh token provided"}, status=400)
        try:
            payload = jwt.decode(refresh_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            user_id = payload.get("user_id")
            if not user_id:
                raise jwt.ExpiredSignatureError("Invalid token")
            user = User.objects.get(id=user_id)
            new_access_token = generate_jwt_token(user)

            return JsonResponse({"access_token": new_access_token})
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Refresh token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid refresh token"}, status=401)


    
    
