from django.db.transaction import atomic
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated


class BaseModelViewSet(viewsets.ModelViewSet):
    serializer_class = None
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = '__all__'
    
    permission_classes  = [IsAuthenticated]

    def paginate_queryset(self, queryset):
        if 'no_page' in self.request.query_params:
            return None

        return super().paginate_queryset(queryset)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'worker': self.request.user})
        return context

    @atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response()
