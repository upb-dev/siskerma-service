from siskerma.app.serializers.base_models_serializer import BaseModelSerializer
from siskerma.app.models import CooperationChoice

class CooperationChoiceSerializer(BaseModelSerializer):
    class Meta:
        model = CooperationChoice
        fields = '__all__'