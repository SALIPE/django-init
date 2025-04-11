from django.contrib import admin
from django.urls import path

from users_app.views import user_auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users', user_auth.UserListView.as_view(), name='user-handles'),
    path('users/user-token', user_auth.UserObtainTokenPairView.as_view(), name='user_token_obtain_pair'),
    path('users/user-token-refresh', user_auth.UserRefreshTokenView.as_view(), name='user_token_refresh'),
    ]
