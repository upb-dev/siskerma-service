import os
import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models
from datetime import datetime
from django.conf import settings


from dateutil.relativedelta import relativedelta

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


# Create your models here.

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(
        reverse('password_reset:reset-password-request'), reset_password_token.key)

    print(reset_password_token.key)


def path_and_rename(instance, filename):

    upload_to = 'siskerma/file'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = f'{instance.pk}.{ext}'
    else:
        # set filename as random string
        filename = f'{uuid.uuid4().hex}.{ext}'
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class BaseFieldModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)

    class Meta:
        abstract = True


class BaseEntryModel(BaseFieldModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('Worker', related_name="%(app_label)s_%(class)s_createdby",
                                   null=True, on_delete=models.SET_NULL, blank=True)
    updated_by = models.ForeignKey('Worker', related_name="%(app_label)s_%(class)s_updatedby",
                                   null=True, on_delete=models.SET_NULL, blank=True)

    class Meta:
        abstract = True


class User(BaseEntryModel):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    address = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=False, validators=[validate_email])
    responsible_name = models.CharField(max_length=125)
    responsible_position = models.CharField(max_length=255)
    responsible_approval_name = models.CharField(max_length=125)
    responsible_approval_position = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    institution = models.ForeignKey(to='Institution', on_delete=models.RESTRICT, null=True)
    cooperation_document = models.ForeignKey(to='CooperationDocument', on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(
        'Worker', related_name='user_createdby', null=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(
        'Worker', related_name='user_updatedby', null=True, on_delete=models.SET_NULL)


class Role(BaseFieldModel):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class WorkerRole(BaseEntryModel):
    worker = models.ForeignKey(to='Worker', on_delete=models.CASCADE)
    role = models.ForeignKey(to=Role, on_delete=models.RESTRICT)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['worker', 'role'], name='unique_worker_role')]


class Worker(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    address = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=15, null=True, default=None, blank=True)
    roles = models.ManyToManyField(to=Role, through=WorkerRole,
                                   through_fields=('worker', 'role'), related_name='workers')
    prodi = models.ForeignKey(to='Prodi', on_delete=models.RESTRICT, null=True)

    @property
    def get_role_name(self):
        return list(self.roles.all().values_list('name', flat=True))


class CooperationChoice(BaseEntryModel):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)


class CooperationDocument(BaseEntryModel):
    TYPE_CHOICE = (
        (1, 'IA'),
        (2, 'MOA'),
        (3, 'MOU')
    )

    PERIOD_CHOICE = (
        (1, 'Berdasar Tanggal'),
        (2, 'Tidak Dibatasi')
    )

    STATUS_CHOICE = (
        (1, 'Draft Pengajuan'),
        (2, 'Disetujui Oleh Kaprodi'),
        (3, 'Disetujui OLeh Dekan'),
        (4, 'Disetujui Oleh Rektor'),
        (5, 'Draft Kadaluarsa'),
        (6, 'Ditolak'),

    )
    number = models.CharField(max_length=125)
    name = models.CharField(max_length=125)
    type = models.IntegerField(choices=TYPE_CHOICE)
    period = models.IntegerField(choices=PERIOD_CHOICE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICE)
    expied_date = models.DateTimeField()
    step = models.IntegerField(default=1)
    choices_set = models.ManyToManyField(to=CooperationChoice, through='CooperationDocumentChoice', through_fields=(
        'document', 'choice'), related_name='cooperationdocument_set')
    # user = models.ForeignKey(to=User, on_delete=models.RESTRICT)
    files = models.ForeignKey(to='CooperationFile', on_delete=models.CASCADE, null=True)
    prodi = models.ForeignKey(to='Prodi', on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        # This means that the model isn't saved to the database yet
        last_id = None
        number = None
        if self._state.adding:
            if self.type == 1:  # type IA
                # Get the maximum display_id value from the database
                last_id = self.prodi.fakultas.last_ai_number
                if last_id is not None:
                    self.prodi.fakultas.last_ai_number = last_id + 1
                    self.prodi.fakultas.save()
                    number = last_id + 1
            if self.type == 2:  # type MOA
                # Get the maximum display_id value from the database
                last_id = self.prodi.fakultas.last_moa_number
                if last_id is not None:
                    self.prodi.fakultas.last_moa_number = last_id + 1
                    self.prodi.fakultas.save()
                    number = last_id + 1

            if self.type == 3:  # type MOU
                # Get the maximum display_id value from the database
                last_id = self.prodi.fakultas.last_mou_number
                if last_id is not None:
                    self.prodi.fakultas.last_mou_number = last_id + 1
                    self.prodi.fakultas.save()
                    number = last_id + 1
            # aggregate can return None! Check it first.
            # If it isn't none, just use the last ID specified (which should be the greatest) and add one to it

            self.number = f"{number:05d}"
            self.expied_date = datetime.now() + relativedelta(months=+6)

        super(CooperationDocument, self).save(*args, **kwargs)


class CooperationFile(BaseEntryModel):
    # coopration_document = models.ForeignKey(to=CooperationDocument, on_delete=models.RESTRICT)
    photo = models.FileField(upload_to=path_and_rename, max_length=255)
    document = models.FileField(upload_to=path_and_rename, max_length=255)
    url = models.URLField()


class CooperationDocumentChoice(BaseEntryModel):
    document = models.ForeignKey(to=CooperationDocument, on_delete=models.CASCADE)
    choice = models.ForeignKey(to=CooperationChoice, on_delete=models.CASCADE)


class Institution(BaseEntryModel):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)


class Fakultas(BaseEntryModel):
    name = models.CharField(max_length=125)
    is_active = models.BooleanField(default=True)
    last_ai_number = models.IntegerField()
    last_moa_number = models.IntegerField()
    last_mou_number = models.IntegerField()


class History(BaseEntryModel):
    document = models.ForeignKey(to=CooperationDocument, on_delete=models.CASCADE)
    label = models.CharField(max_length=125, default='Pengajuan')
    number = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if self._state.adding:
            last_number = History.objects.all().aggregate(largest=models.Max('number'))['largest']

            if last_number is not None:
                self.number = last_number + 1
            else:
                self.number = 1

        super(History, self).save(*args, **kwargs)

    class Meta:
        ordering = ['number']


class HistoryDetail(BaseEntryModel):
    STATUS_CHOICE = (
        (1, 'Disetujui'),
        (2, 'Ditolak'),

    )
    history = models.ForeignKey(to=History, on_delete=models.CASCADE)
    key = models.CharField(max_length=125)
    date = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=125, null=True)
    status = models.IntegerField(choices=STATUS_CHOICE)

    class Meta:
        ordering = ['created_at']


class Prodi(BaseEntryModel):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    fakultas = models.ForeignKey(to=Fakultas, on_delete=models.RESTRICT)
