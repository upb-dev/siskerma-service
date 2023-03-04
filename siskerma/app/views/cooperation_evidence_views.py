from django.db.transaction import atomic

from siskerma.app.filters.file_filter import FileFIlter
from siskerma.app.models import CooperationEvidence
from siskerma.app.serializers.cooperation_evidence_serializer import \
    CooperationEvidenceSerializer
from siskerma.app.views.base_model_viewset import BaseModelViewSet


class CooperationEvidenceViewSet(BaseModelViewSet):
    queryset = CooperationEvidence.objects.all()
    serializer_class = CooperationEvidenceSerializer
    filterset_class = FileFIlter

    @atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @atomic
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
