from siskerma.app.views.base_model_viewset import BaseModelViewSet
from siskerma.app.serializers.fakultas_serializers import FakultasSerializer
from siskerma.app.models import Fakultas


class FakultasViewSet(BaseModelViewSet):
    queryset = Fakultas.objects.all()
    serializer_class = FakultasSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)