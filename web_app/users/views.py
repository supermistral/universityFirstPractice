from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import (
    UserSerializer, UserProfileSerializer, CustomTokenObtainPairSerializer
)
from .permissions import UserProfilePermission, SuperuserPermission
from rest_framework_simplejwt.views import TokenObtainPairView


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, UserProfilePermission]
    
    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, SuperuserPermission]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer