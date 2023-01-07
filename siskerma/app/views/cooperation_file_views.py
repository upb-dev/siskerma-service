from siskerma.app.filters.file_filter import FileFIlter
from siskerma.app.models import CooperationFile
from siskerma.app.serializers.cooperation_file_serializer import CooperationFileSerializer
from siskerma.app.views.base_model_viewset import BaseModelViewSet
from django.db.transaction import atomic


class CooperationFileVIewSet(BaseModelViewSet):
    queryset = CooperationFile.objects.all()
    serializer_class = CooperationFileSerializer
    filterset_class = FileFIlter

    @atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
