import django_filters
from siskerma.app.filters.list_filter import ListFilter
from siskerma.app.models import CooperationDocument


class DashboardFilter(django_filters.FilterSet):
    fakultas = django_filters.CharFilter(field_name='prodi__fakultas__id',  lookup_expr='iexact')
    prodi = django_filters.CharFilter(field_name='prodi_id',  lookup_expr='iexact')

    class Meta:
        model = CooperationDocument
        fields = '__all__'
