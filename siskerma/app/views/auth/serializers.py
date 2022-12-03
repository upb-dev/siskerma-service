from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data = {}

        data["refresh_token"] = str(refresh)
        data["access_token"] = str(refresh.access_token)
        data["expires_in"] = 86400
        data["user_id"] = refresh['user_id']
        data["user_email"] = self.user.email
        data["user_name"] = self.user.first_name
        data["roles"] = list(self.user.roles.all().values_list('name', flat=True))

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
