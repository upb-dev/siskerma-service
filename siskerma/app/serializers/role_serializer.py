from rest_framework import serializers
from siskerma.app.models import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
