from rest_framework import serializers
from datetime import datetime
import pytz
from siskerma.app.models import CooperationChoice, CooperationDocument, CooperationDocumentChoice, Fakultas, Institution, Prodi


def convert_date(date: str):
    convert_date = datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d-%H:%M:%S")
    convert_date = datetime.strptime(convert_date, "%Y-%m-%d-%H:%M:%S")
    convert_date = datetime(year=convert_date.year, month=convert_date.month, day=convert_date.day,
                            hour=convert_date.hour, minute=convert_date.minute, second=convert_date.second,
                            microsecond=convert_date.microsecond, tzinfo=pytz.timezone('etc/GMT-7'))

    return str(convert_date)


def get_query_params(self, instance):
    filter_set = {}
    if self.context['request'].query_params.get('created_at__gte') is not None:
        filter_set['created_at__gte'] = convert_date(self.context['request'].query_params.get('created_at__gte'))

    if self.context['request'].query_params.get('created_at__lte') is not None:
        filter_set['created_at__lte'] = convert_date(self.context['request'].query_params.get('created_at__lte'))

    return filter_set


class DocumentByChoice(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    count = serializers.SerializerMethodField()

    def get_count(self, instance):
        document_by_choice = CooperationDocumentChoice.objects.filter(choice=instance)
        return document_by_choice.distinct().count()

    class Meta:
        model = CooperationDocumentChoice
        fields = ['count', 'name']


class FakultasDataSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    count = serializers.SerializerMethodField()

    def get_count(self, instance):
        document_data = CooperationDocument.objects.filter(prodi__fakultas=instance, status=3)

        return document_data.distinct().count()

    class Meta:
        model = Fakultas
        fields = ['count', 'name']


class ProdiDataSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    count = serializers.SerializerMethodField()

    def get_count(self, instance):
        data = CooperationDocument.objects.filter(prodi=instance, status=3)
        return data.distinct().count()

    class Meta:
        model = Prodi
        fields = ['name', 'count']


class DashboardSerializer(serializers.Serializer):
    choice_data = serializers.SerializerMethodField()
    fakultas_data = serializers.SerializerMethodField()
    prodi_data = serializers.SerializerMethodField()
    headers = serializers.SerializerMethodField()

    def get_choice_data(self, obj):
        choice_data = CooperationChoice.objects.all()
        data = DocumentByChoice(instance=choice_data, many=True)
        return data.data

    def get_fakultas_data(self, obj):
        fakultas = Fakultas.objects.all()
        data = FakultasDataSerializer(instance=fakultas, many=True)
        return data.data

    def get_prodi_data(self, obj):
        prodi = Prodi.objects.all()
        data = ProdiDataSerializer(instance=prodi, many=True)
        return data.data

    def get_headers(self, instance):
        filter_set = get_query_params(self, instance)

        total_ia = CooperationDocument.objects.filter(**filter_set, type=1).exclude(status=0)
        total_moa = CooperationDocument.objects.filter(**filter_set, type=2).exclude(status=0)
        total_mou = CooperationDocument.objects.filter(**filter_set, type=3).exclude(status=0)

        data_valid = CooperationDocument.objects.filter(**filter_set, status=3)
        data_belum_divalidasi = CooperationDocument.objects.filter(**filter_set, status=1)
        data_ditolak = CooperationDocument.objects.filter(**filter_set, status=5)

        headers = {
            "total_ia": total_ia.distinct().count(),
            "total_moa": total_moa.distinct().count(),
            "total_mou": total_mou.distinct().count(),
            "data_valid": data_valid.distinct().count(),
            "data_belum_divalidasi": data_belum_divalidasi.distinct().count(),
            "data_ditolak": data_ditolak.distinct().count()
        }

        return headers
