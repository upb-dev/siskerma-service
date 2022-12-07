from siskerma.app.views.base_model_viewset import BaseModelViewSet
from siskerma.app.serializers.cooperation_document_serializers import CooperationDocumentSerializer
from siskerma.app.models import CooperationDucument


class CooperationDocumentViewSet(BaseModelViewSet):
    queryset = CooperationDucument.objects.all()
    serializer_class = CooperationDocumentSerializer

    def get_queryset(self):
        self.queryset = self.queryset.filter(user__is_active=True)
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
