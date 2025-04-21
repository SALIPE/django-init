from content import views
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from users.views import adresses, user_auth, users

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin', admin.site.urls),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users', users.ListUsers.as_view(), name='user-list'),
    # Public User Authentication Routes
    path('users/login', user_auth.UserObtainTokenPairView.as_view(), name='user_token_obtain_pair'),
    path('users/refresh-token', user_auth.UserRefreshTokenView.as_view(), name='user_token_refresh'),
    # User Methods
    path('users', users.PublicUserCreationView.as_view(), name='user-handles'),
    path('users/by-token', users.UserDetailAPIView.as_view(), name='user-by-token'),
    # Content Routes
    path('content/', views.ContentView.as_view(), name='cont'),
    #Addresses Routes
    path('addresses/cities/<str:state_id>', adresses.CityByState.as_view(), name='cities-by-state'),
    path('addresses/states', adresses.ListStates.as_view(), name='state-list-all'),
    ]
