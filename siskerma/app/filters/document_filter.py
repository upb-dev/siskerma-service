import django_filters
from siskerma.app.models import CooperationDocument
from siskerma.app.filters.list_filter import ListFilter


class DocumentFilter(django_filters.FilterSet):
    ajuan_pribadi = django_filters.CharFilter(field_name='created_by__id', lookup_expr='iexact')
    fakultas = django_filters.CharFilter(field_name='prodi__fakultas__id', lookup_expr='iexact')
    prodi = django_filters.CharFilter(field_name='prodi__id')
    lembaga = ListFilter(field_name='user__institution__id', distinct=True)
    # unfinish = django_filters.BooleanFilter(field_name='evidence', lookup_expr='isnull')
    finish = django_filters.BooleanFilter(field_name='evidence', lookup_expr='isnull', exclude=True)
    #  TODO filter 1 / 2 month
    class Meta:
        model = CooperationDocument
        fields = '__all__'
