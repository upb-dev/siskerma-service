from siskerma.app.views.base_model_viewset import BaseModelViewSet
from siskerma.app.serializers.institution_serializer import InstitutionSerializer
from siskerma.app.models import Institution


class InstitutionViewSet(BaseModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)