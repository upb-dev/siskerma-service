import django_filters
from siskerma.app.models import CooperationEvidence


class FileFIlter(django_filters.FilterSet):

    class Meta:
        model = CooperationEvidence
        
        exclude = ['photo']
