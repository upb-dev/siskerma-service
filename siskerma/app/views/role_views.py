from siskerma.app.permisson import AdminPermission
from siskerma.app.serializers.role_serializer import RoleSerializer

from siskerma.app.views.base_model_viewset import BaseModelViewSet
from siskerma.app.models import Role


class RoleViewSet(BaseModelViewSet):
    queryset = Role.objects.all().order_by('name')
    serializer_class = RoleSerializer

    def get_permissions(self):
        if self.action.lower() in ['create', 'update', 'destroy']:
            self.permission_classes = [AdminPermission]
        return super().get_permissions()

    def get_queryset(self):
        if self.request.user and ('Admin' not in self.request.user.get_role_name):
            self.queryset = self.queryset.filter(is_active=True)
        return super().get_queryset()
