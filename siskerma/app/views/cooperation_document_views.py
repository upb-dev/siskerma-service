from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.db.transaction import atomic
from django.http import HttpResponse
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response

from siskerma.app.filters.document_filter import DocumentFilter
from siskerma.app.models import CooperationDocument
from siskerma.app.serializers.cooperation_document_serializers import (
    AjukanSerializer, AjukanUlangSerializer, CooperationDocumentSerializer, ImportDataSerializer,
    ListCooperationDocumentSerializer, SetReferenceSerializer)
from siskerma.app.serializers.history_serializers import \
    HistoryDetailSerializer
from siskerma.app.views.base_model_viewset import BaseModelViewSet


class CooperationDocumentViewSet(BaseModelViewSet):
    queryset = CooperationDocument.objects.all().order_by('created_at')
    serializer_class = CooperationDocumentSerializer
    filterset_class = DocumentFilter
    search_fields = ['name', 'number', 'document_number', 'user__name',
                     'user__responsible_name', 'user__responsible_approval_name', 'user__email']

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
            if self.request.user and ('Dosen' in self.request.user.get_role_name or 'Mahasiswa' in self.request.user.get_role_name):
                self.queryset = self.queryset.filter(created_by=self.request.user)

        if 'is_active' in self.request.query_params:
            self.queryset = self.queryset.filter(Q(end_date__gte=datetime.now()) | Q(date_end__gte=datetime.now()))

        if 'is_pribadi' in self.request.query_params:
            self.queryset = self.queryset.filter(created_by=self.request.user)

        if 'referensi' in self.request.query_params:
            self.queryset = self.queryset.filter(parent__isnull=True).exclude(type=3)

        if 'periode' in self.request.query_params:
            if self.request.query_params['periode'] == '1':
                self.queryset = self.queryset.filter(end_date__gte=datetime.now(
                ), end_date__lte=datetime.now() + relativedelta(months=+1))
            if self.request.query_params['periode'] == '2':
                self.queryset = self.queryset.filter(end_date__gte=datetime.now(
                ), end_date__lte=datetime.now() + relativedelta(months=+2))

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

    @atomic
    @action(detail=True, methods=['POST'], url_path='ajukan')
    def ajukan(self, request, *args, **kwargs):
        data = self.get_object()
        serializer = AjukanSerializer(context=self.get_serializer_context())
        serializer.ajukan(instance=data)

        return Response()

    @atomic
    @action(detail=True, methods=['POST'], url_path='set-reference')
    def set_reference(self, request, *args, **kwargs):
        data = self.get_object()
        serializer = SetReferenceSerializer(data=self.request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.set_referenc(instance=data, validated_data=serializer.validated_data)

        return Response()

    @atomic
    @action(detail=False, methods=['GET'], url_path='check-expired')
    def check_expired(self, request, *args, **kwargs):
        data = CooperationDocument.objects.filter(status=0, expied_date__lte=datetime.now())

        for i in data:
            i.status = 5
            i.save()

        return Response()

    @action(detail=False, methods=['GET'], url_path='export')
    def export(self, request, *args, **kwargs):
        from siskerma.app.helpers.queryset_to_workbook import \
            queryset_to_workbook
        columns = (
            'document_number',
            'name',
            'type',
            'status',
        )

        queryset = self.filter_queryset(self.queryset)
        workbook = queryset_to_workbook(queryset, columns)
        response = HttpResponse(
            content=workbook,  content_type='aapplication/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="export {}.xlsx"'.format(str(datetime.now()))
        return response

    @action(detail=False, methods=['POST'], url_path='upload_data')
    def upload_data(self, request, *args, **kwargs):
        serializer = ImportDataSerializer(data=self.request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.insert_data(file=serializer.validated_data)

        return Response()
