from siskerma.app.views.base_model_viewset import BaseModelViewSet
from siskerma.app.serializers.user_serializers import UserSerializer
from siskerma.app.models import User


class UserViewSet(BaseModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)