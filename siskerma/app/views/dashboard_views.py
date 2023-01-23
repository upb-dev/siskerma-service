from rest_framework import viewsets
from siskerma.app.filters.document_filter import DocumentFilter
from siskerma.app.models import CooperationDocument
from rest_framework.decorators import action
from rest_framework.response import Response

from siskerma.app.serializers.dashboard_serializers import DashboardSerializer


class DashBoardViewSet(viewsets.GenericViewSet):
    queryset = CooperationDocument.objects.all()
    serializer_class = DashboardSerializer

    @action(detail=False, methods=['GET'], url_path='get-info')
    def get_info(self, reruest, *args, **kwargs):
        self.filterset_class = DocumentFilter

        queryset = self.filter_queryset(self.queryset)

        serializer = self.get_serializer(instance=queryset, context=self.get_serializer_context())

        return Response(serializer.data)
