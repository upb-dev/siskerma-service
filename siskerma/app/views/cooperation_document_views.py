from siskerma.app.filters.document_filter import DocumentFilter
from siskerma.app.serializers.history_serializers import HistoryDetailSerializer
from siskerma.app.views.base_model_viewset import BaseModelViewSet
from siskerma.app.serializers.cooperation_document_serializers import AjukanUlangSerializer, CooperationDocumentSerializer, ListCooperationDocumentSerializer
from siskerma.app.models import CooperationDocument
from django.db.transaction import atomic
from rest_framework.decorators import action
from rest_framework.response import Response


class CooperationDocumentViewSet(BaseModelViewSet):
    queryset = CooperationDocument.objects.all().order_by('created_at')
    serializer_class = CooperationDocumentSerializer
    filterset_class = DocumentFilter
    search_fields = ['name', 'number',]

    def get_queryset(self):
        if self.request.user and ('Admin' not in self.request.user.get_role_name):
            if self.request.user and ('Rektor' in self.request.user.get_role_name):
                # if 'validasi' in self.request.query_params:
                #     self.queryset = self.queryset.filter(type__in=[3])
                self.queryset = self.queryset
            if self.request.user and ('Dekan' in self.request.user.get_role_name):
                self.queryset = self.queryset.filter(prodi__fakultas__name=self.request.user.prodi.fakultas.name)
                # if 'validasi' in self.request.query_params:
                #     self.queryset = self.queryset.filter(type__in=[2, 3])
            if self.request.user and ('Kaprodi' in self.request.user.get_role_name):
                self.queryset = self.queryset.filter(prodi__name=self.request.user.prodi.name, )
                # if 'validasi' in self.request.query_params:
                #     self.queryset = self.queryset.filter(type__in=[1, 2, 3])
            if self.request.user and ('Dosen' or 'Mahasiswa' in self.request.user.get_role_name):
                self.queryset = self.queryset.filter(created_by=self.request.user)

        if 'is_pribadi' in self.request.query_params:
            self.queryset = self.queryset.filter(created_by=self.request.user)

        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action.lower() == 'list':
            self.serializer_class = ListCooperationDocumentSerializer
        return super().get_serializer_class()

    @atomic
    @action(detail=True, methods=['POST'], url_path='validasi')
    def validasi(self, request, *args, **kwargs):
        data = self.get_object()
        serializer = HistoryDetailSerializer(data=self.request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.validasi_ajuan(obj=data, validated_data=serializer.validated_data)

        return Response()

    @atomic
    @action(detail=True, methods=['POST'], url_path='ajukan-ulang')
    def ajukan_ulang(self, *args, **kwargs):
        data = self.get_object()

        serializer = AjukanUlangSerializer(context=self.get_serializer_context())
        serializer.ajukan_ulang(obj=data)

        return Response()
