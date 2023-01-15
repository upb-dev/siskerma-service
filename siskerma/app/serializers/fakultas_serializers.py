from siskerma.app.serializers.base_models_serializer import BaseModelSerializer
from siskerma.app.models import Fakultas


class FakultasSerializer(BaseModelSerializer):

    class Meta:
        model = Fakultas
        fields = ['id', 'name', 'is_active', 'created_by', 'updated_by', 'created_at', 'updated_at']
