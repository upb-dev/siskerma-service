from django.urls import re_path, include
from rest_framework import routers
from siskerma.app.views.cooperation_file_views import CooperationFileVIewSet

from siskerma.app.views.fakultas_views import FakultasViewSet
from siskerma.app.views.role_views import RoleViewSet
from siskerma.app.views.worker_views import WorkerViewSet
from siskerma.app.views.cooperation_document_views import CooperationDocumentViewSet
from siskerma.app.views.cooperation_choice_views import CooperationChoiceViewSet
from siskerma.app.views.fakultas_views import FakultasViewSet
from siskerma.app.views.institution_views import InstitutionViewSet
from siskerma.app.views.prodi_views import ProdiViewSet
from siskerma.app.views.user_views import UserViewSet


router = routers.DefaultRouter()

router.register('fakultas', FakultasViewSet)
router.register('worker', WorkerViewSet)
router.register('role', RoleViewSet)
router.register('kerja_sama', CooperationDocumentViewSet)
router.register('bentuk_kerjasama', CooperationChoiceViewSet)
router.register('institution', InstitutionViewSet)
router.register('prodi', ProdiViewSet)
router.register('fakultas', FakultasViewSet)
router.register('user', UserViewSet)
router.register('file', CooperationFileVIewSet)


urlpatterns = [
    re_path('', include('siskerma.app.views.auth.urls')),
    re_path('', include(router.urls)),
] 
