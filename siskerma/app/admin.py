from django.contrib import admin

# Register your models here.
from siskerma.app.models import *

admin.site.register([CooperationChoice, CooperationDocumentChoice, CooperationDucument,
                    User, Fakultas, Prodi, Role, Worker, CooperationFile, Institution, WorkerRole])
