from django.urls import path
from .views import (
    UserCreateView, UserListView, UserProfileView, CustomTokenObtainPairView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('create/', UserCreateView.as_view(), name="user_create"),
    path('profile/', UserProfileView.as_view(), name="user_profile"),
    path('user-list/', UserListView.as_view(), name="user_list"),
    path('token/', CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
]