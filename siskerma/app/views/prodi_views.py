from siskerma.app.views.base_model_viewset import BaseModelViewSet
from siskerma.app.serializers.prodi_serializers import ProdiSerializer
from siskerma.app.models import Prodi


class ProdiViewSet(BaseModelViewSet):
    queryset = Prodi.objects.all()
    serializer_class = ProdiSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)