from siskerma.app.serializers.base_models_serializer import BaseModelSerializer
from siskerma.app.models import Institution

class InstitutionSerializer(BaseModelSerializer):
    class Meta:
        model = Institution
        fields = '__all___'