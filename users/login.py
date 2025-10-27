from django.contrib.auth import get_user_model
from .models import LoginCode
import secrets
import string
from django.contrib.sites.shortcuts import get_current_site
from .tasks import send_auth_code
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

class LoginWithAuthCodeUseCase:
    def __init__(self, request):
        self.request = request

    def execute(self, email: str):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response("Пользователя не найдено", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        auth_code = self._generate_auth_code()
        self._save_auth_code(user, auth_code)
        self._send_auth_code(user, auth_code)


    def _generate_auth_code(self):
        return "".join(secrets.choice(string.digits) for _ in range(6))
    
    def _save_auth_code(self, user, auth_code):
        LoginCode.objects.create(user=user, code=auth_code)

    def _send_auth_code(self, user, auth_code):
        email = user.email
        current_site = get_current_site(self.request)
        send_auth_code.delay(
            domain=current_site.domain,
            email=email,
            auth_code=auth_code
            )
    
        

class LoginUseCase:
    def __init__(self, auth_code: str, email: str):
        self.auth_code=auth_code
        self.email=email

    def execute(self):
        try:
            login_code=LoginCode.objects.filter(code=self.auth_code, user__email=self.email, used_at__isnull=True).order_by('-created_at')[0]
        except IndexError:
            return {}
        
        if timezone.now() > login_code.created_at + self._get_time_experation_code():
            return {}
        
        if login_code.used_at:
            return {}
        
        login_code.used_at = timezone.now()
        login_code.save()

        refresh = RefreshToken.for_user(login_code.user)
        return {
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        }

    def _get_time_experation_code(self):
        return timedelta(minutes=5)
        
