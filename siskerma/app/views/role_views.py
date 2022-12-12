from siskerma.app.permisson import AdminPermission
from siskerma.app.serializers.role_serializer import RoleSerializer

from siskerma.app.views.base_model_viewset import BaseModelViewSet
from siskerma.app.models import Role


class RoleViewSet(BaseModelViewSet):
    queryset = Role.objects.filter(is_active=True)
    serializer_class = RoleSerializer

    def get_permissions(self):
        if self.action.lower() in ['create', 'update', 'destroy']:
            self.permission_classes = [AdminPermission]
        return super().get_permissions()
