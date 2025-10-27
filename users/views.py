from django.contrib.auth import get_user_model, login
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from .serializers import UserCreateSerializer, UserSerializer, GetConfirmationCodeSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .login import LoginWithAuthCodeUseCase, LoginUseCase

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        use_case = LoginWithAuthCodeUseCase(request)

        try:
            use_case.execute(
                email=serializer.validated_data['email']
                )
        except Exception as e:
            return Response("Ошибка", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response("Отправили письмо с кодом", status=status.HTTP_200_OK)
    
class LoginView(viewsets.GenericViewSet):
    @action(
        methods=['post'],
        detail=False,
        url_path='get-confirmation-code',
        serializer_class=GetConfirmationCodeSerializer
    )
    def get_email_confirmation_code(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = LoginWithAuthCodeUseCase(request)

        try:
            use_case.execute(
                email=serializer.validated_data['email']
                )
        except Exception as e:
            return Response("Ошибка", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response("Отправили письмо с кодом", status=status.HTTP_200_OK)
        
    @action(
            methods=['get'],
            detail=False,
            url_path='login',
            serializer_class=LoginSerializer,
    )
    def login(self, request):
        query_params = request.query_params
        serializer = self.get_serializer(data=query_params)
        serializer.is_valid(raise_exception=True)

        try:
            auth_data = LoginUseCase(
                auth_code=serializer.validated_data['auth_code'],
                email=serializer.validated_data['email']
            ).execute()
        except Exception as e:
            return Response("Ошибка", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(auth_data, status=status.HTTP_200_OK)

    
