import django_filters
from siskerma.app.models import CooperationDocument


class DocumentFilter(django_filters.FilterSet):
    ajuan_pribadi = django_filters.CharFilter(field_name='created_by__id', lookup_expr='iexact')
    fakultas = django_filters.CharFilter(field_name='fakultas__id', lookup_expr='iexact')
    prodi = django_filters.CharFilter(field_name='fakultas__prodi_set_id')

    class Meta:
        model = CooperationDocument
        fields = '__all__'
