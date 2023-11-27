from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, UserSerializer
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics
from rest_framework import viewsets
from .permissions import IsSuperuser, IsUserOwnerOrStaff

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()

        if not self.request.user.is_superuser:
            queryset = queryset.filter(is_staff=False)

        return queryset
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated(), IsUserOwnerOrStaff()]
        
        if self.action in ['create']:
            return [IsSuperuser()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsUserOwnerOrStaff()]
        return super().get_permissions()
    
class RegisterAPI(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    serializer_class = RegisterSerializer
    permission_classes = []
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data        
        return Response({'success': 'Successfully created','user':user_data}, status=status.HTTP_201_CREATED)
    

class LoginAPI(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    serializer_class = LoginSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({'detail': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST) 
