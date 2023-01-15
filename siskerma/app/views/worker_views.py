from siskerma.app.models import Worker
from siskerma.app.permisson import AdminPermission
from siskerma.app.serializers.change_password_serializers import ChangePasswordSerializer
from siskerma.app.serializers.worker_serializer import WorkerSerializer
from rest_framework import viewsets, filters
from rest_framework.response import Response
from django.db.transaction import atomic
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend


class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.filter(is_active=True).order_by('date_joined')
    serializer_class = WorkerSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['username', 'address', 'phone', 'email']

    def get_permissions(self):
        method = self.request.method.lower()

        if self.action_map.get(method) in ['create', 'update', 'destroy']:
            self.permission_classes = [AdminPermission]
        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        instance: Worker = self.get_object()
        instance.is_active = False

        instance.save()
        serializers = self.get_serializer(instance)

        return Response(serializers.data)

    @atomic
    @action(detail=True, methods=['POST'], url_path='change-password')
    def change_password(self, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(self.get_object(), serializer.validated_data)

        return Response()
