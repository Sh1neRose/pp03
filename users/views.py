from django.contrib.auth import get_user_model, login
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from .serializers import UserCreateSerializer, UserSerializer, UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        if self.action == 'login':
            return UserLoginSerializer
        return UserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response_data = {
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    @action(
            methods=['post'],
            detail=False,
            url_path='login',
            )
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        refresh = RefreshToken.for_user(user)
        response_data = {
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)