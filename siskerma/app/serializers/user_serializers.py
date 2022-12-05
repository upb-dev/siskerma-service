from siskerma.app.serializers.base_models_serializer import BaseModelSerializer
from siskerma.app.models import User

class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = '__all__'