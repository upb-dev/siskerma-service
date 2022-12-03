from django.urls import re_path, include
from rest_framework import routers

from siskerma.app.views.fakultas_views import FakultasViewSet
from siskerma.app.views.role_views import RoleViewSet
from siskerma.app.views.worker_views import WorkerViewSet
from siskerma.app.views.cooperation_document_views import CooperationDocumentViewSet

router = routers.DefaultRouter()

router.register('fakultas', FakultasViewSet)
router.register('worker', WorkerViewSet)
router.register('role', RoleViewSet)
router.register('kerja_sama', CooperationDocumentViewSet)

urlpatterns = [
    re_path('', include('siskerma.app.views.auth.urls')),
    re_path('', include(router.urls)),
]