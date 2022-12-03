from siskerma.app.serializers.base_models_serializer import BaseModelSerializer
from siskerma.app.models import CooperationFile

class CooperationFileSerializer(BaseModelSerializer):
    class Meta:
        model = CooperationFile
        fields = '__all__'