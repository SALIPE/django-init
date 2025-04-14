from content import views
from users.views import user_auth, users

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    # Public User Authentication Routes
    path('users/login', user_auth.UserObtainTokenPairView.as_view(), name='user_token_obtain_pair'),
    path('users/refresh-token', user_auth.UserRefreshTokenView.as_view(), name='user_token_refresh'),
    # User Methods
    path('users/', users.PublicUserCreationView.as_view(), name='user-handles'),
    path('users/<int:pk>/', users.UserDetailAPIView.as_view(), name='user-detail'),
    # Content Routes
    path('content/', views.TestContentView.as_view(), name='cont'),
    ]
