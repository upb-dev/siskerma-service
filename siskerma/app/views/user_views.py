from siskerma.app.views.base_model_viewset import BaseModelViewSet
from siskerma.app.serializers.user_serializers import UserSerializer
from siskerma.app.models import User


class UserViewSet(BaseModelViewSet):
    queryset = User.objects.all().order_by('created_at')
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user and ('Admin' not in self.request.user.get_role_name):
            self.queryset = self.queryset.filter(is_active=True)
        return super().get_queryset()
