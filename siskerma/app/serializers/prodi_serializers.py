from siskerma.app.serializers.base_models_serializer import BaseModelSerializer
from siskerma.app.models import Fakultas, Prodi
from rest_framework import serializers

from siskerma.app.serializers.fakultas_serializers import FakultasSerializer


class ProdiSerializer(BaseModelSerializer):
    fakultas_id = serializers.PrimaryKeyRelatedField(
        queryset=Fakultas.objects.all(), write_only=True, allow_empty=True, source='fakultas')

    fakultas = FakultasSerializer(read_only=True)

    def create(self, validated_data):
        data = validated_data
        return super().create(validated_data)

    class Meta:
        model = Prodi
        fields = '__all__'
