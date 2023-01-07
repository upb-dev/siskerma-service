import django_filters
from siskerma.app.models import CooperationFile


class FileFIlter(django_filters.FilterSet):

    class Meta:
        model = CooperationFile
        exclude = ['photo', 'document']
