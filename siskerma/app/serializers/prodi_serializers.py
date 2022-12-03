from siskerma.app.serializers.base_models_serializer import BaseModelSerializer
from siskerma.app.models import Prodi

class ProdiSerializer(BaseModelSerializer):
    class Meta:
        model = Prodi
        fields = '__all__'
    