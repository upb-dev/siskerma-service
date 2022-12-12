from siskerma.app.permisson import AdminPermission
from siskerma.app.views.base_model_viewset import BaseModelViewSet
from siskerma.app.serializers.cooperation_choice_serializers import CooperationChoiceSerializer
from siskerma.app.models import CooperationChoice


class CooperationChoiceViewSet(BaseModelViewSet):
    queryset = CooperationChoice.objects.all()
    serializer_class = CooperationChoiceSerializer

    def get_permissions(self):
        if self.action.lower() in ['create', 'update', 'destroy']:
            self.permission_classes = [AdminPermission]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)