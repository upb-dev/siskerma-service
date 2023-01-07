import django_filters
from siskerma.app.models import CooperationDucument


class DocumentFilter(django_filters.FilterSet):
    ajuan_pribadi = django_filters.CharFilter(field_name='created_by__id', lookup_expr='iexact')

    class Meta:
        model = CooperationDucument
        fields = '__all__'
