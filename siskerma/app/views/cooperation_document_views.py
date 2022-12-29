from siskerma.app.views.base_model_viewset import BaseModelViewSet
from siskerma.app.serializers.cooperation_document_serializers import CooperationDocumentSerializer, ListCooperationDocumentSerializer
from siskerma.app.models import CooperationDucument


class CooperationDocumentViewSet(BaseModelViewSet):
    queryset = CooperationDucument.objects.all().order_by('created_at')
    serializer_class = CooperationDocumentSerializer

    def get_queryset(self):
        if self.request.user and ('Admin' not in self.request.user.get_role_name):
            self.queryset = self.queryset.filter(created_by=self.request.user)
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action.lower() == 'list':
            self.serializer_class = ListCooperationDocumentSerializer
        return super().get_serializer_class()
