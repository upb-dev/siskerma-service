from siskerma.app.serializers.base_models_serializer import BaseModelSerializer
from siskerma.app.models import CooperationDucument

class CooperationDocumentSerializer(BaseModelSerializer):
    class Meta:
        model = CooperationDucument
        fields = '__all__'