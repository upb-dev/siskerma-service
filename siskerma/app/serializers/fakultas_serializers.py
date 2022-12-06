from siskerma.app.serializers.base_models_serializer import BaseModelSerializer
from siskerma.app.models import Fakultas


class FakultasSerializer(BaseModelSerializer):
    class Meta:
        model = Fakultas
        fields = '__all__'
