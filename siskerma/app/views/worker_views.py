from siskerma.app.models import Worker
from siskerma.app.permisson import AdminPermission
from siskerma.app.serializers.worker_serializer import WorkerSerializer
from rest_framework import viewsets
from rest_framework.response import Response


class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.filter(is_active=True).order_by('date_joined')
    serializer_class = WorkerSerializer

    def get_permissions(self):
        if self.action.lower() in ['create', 'update', 'destroy']:
            self.permission_classes = [AdminPermission]
        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        instance: Worker = self.get_object()
        instance.is_active = False

        instance.save()
        serializers = self.get_serializer(instance)

        return Response(serializers.data)
