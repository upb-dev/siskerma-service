
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from django.urls import re_path


urlpatterns = [
    re_path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
