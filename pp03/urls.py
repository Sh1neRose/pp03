from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users.views import UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/', include([
        path('', include(router.urls)),
        path('token/', include([
            path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
            path('refresh/', TokenRefreshView.as_view(), name='token_refresh')
        ])),
    ])),
    path('admin/', admin.site.urls),
]
