from siskerma.app.models import Prodi, Role, Worker
from rest_framework import serializers
from siskerma.app.serializers.prodi_serializers import ProdiSerializer

from siskerma.app.serializers.role_serializer import RoleSerializer


class WorkerSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(
    ), many=True, write_only=True, source='roles', required=False)
    roles = RoleSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True, required=False,)
    prodi_id = serializers.PrimaryKeyRelatedField(
        queryset=Prodi.objects.all(), write_only=True, source='prodi', required=False)
    prodi = ProdiSerializer(read_only=True)

    class Meta:
        model = Worker
        fields = '__all__'

    def validate_password(self, attrs):
        from django.contrib.auth.hashers import make_password
        return make_password(attrs)

    def update(self, instance: Worker, validated_data):
        validated_data['password'] = instance.password
        return super().update(instance, validated_data)
