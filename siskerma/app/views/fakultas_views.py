from siskerma.app.permisson import AdminPermission
from siskerma.app.views.base_model_viewset import BaseModelViewSet
from siskerma.app.serializers.fakultas_serializers import FakultasSerializer
from siskerma.app.models import Fakultas


class FakultasViewSet(BaseModelViewSet):
    queryset = Fakultas.objects.all()
    serializer_class = FakultasSerializer

    def get_permissions(self):
        if self.action.lower() in ['create', 'update', 'destroy']:
            self.permission_classes = [AdminPermission]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
