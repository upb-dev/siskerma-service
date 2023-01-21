import django_filters
from siskerma.app.filters.list_filter import ListFilter
from siskerma.app.models import Worker


class WorkerFilter(django_filters.FilterSet):
    prodi = django_filters.CharFilter(field_name='prodi__name', lookup_expr='iexact')
    fakultas = django_filters.CharFilter(field_name='prodi__fakultas__name', lookup_expr='iexact')
    roles = ListFilter(field_name='roles')

    class Meta:
        model: Worker
        fields = '__all__'
