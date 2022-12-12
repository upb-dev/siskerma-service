from siskerma.app.permisson import AdminPermission
from siskerma.app.views.base_model_viewset import BaseModelViewSet
from siskerma.app.serializers.prodi_serializers import ProdiSerializer
from siskerma.app.models import Prodi


class ProdiViewSet(BaseModelViewSet):
    queryset = Prodi.objects.all()
    serializer_class = ProdiSerializer

    def get_permissions(self):
        if self.action.lower() in ['create', 'update', 'destroy']:
            self.permission_classes = [AdminPermission]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)