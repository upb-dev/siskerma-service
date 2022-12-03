from siskerma.app.models import Role, Worker
from rest_framework import serializers

from siskerma.app.serializers.role_serializer import RoleSerializer


class WorkerSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(
    ), many=True, write_only=True, source='roles', required=False)
    roles = RoleSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Worker
        fields = '__all__'

    def validate_password(self, attrs):
        from django.contrib.auth.hashers import make_password
        return make_password(attrs)
