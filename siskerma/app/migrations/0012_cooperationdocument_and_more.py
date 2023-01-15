# Generated by Django 4.1.3 on 2023-01-14 10:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_history_options_alter_historydetail_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='CooperationDocument',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('number', models.CharField(max_length=125)),
                ('name', models.CharField(max_length=125)),
                ('type', models.IntegerField(choices=[(1, 'IA'), (2, 'MOA'), (3, 'MOU')])),
                ('period', models.IntegerField(choices=[(1, 'Berdasar Tanggal'), (2, 'Tidak Dibatasi')])),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('date_end', models.DateField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Draft Pengajuan'), (2, 'Disetujui Oleh Kaprodi'), (3, 'Disetujui OLeh Dekan'), (4, 'Disetujui Oleh Rektor'), (5, 'Draft Kadaluarsa'), (6, 'Ditolak')])),
                ('expied_date', models.DateTimeField()),
                ('step', models.IntegerField(default=1)),
                ('choices_set', models.ManyToManyField(related_name='cooperationdocument_set', through='app.CooperationDocumentChoice', to='app.cooperationchoice')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('files', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.cooperationfile')),
                ('prodi', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.prodi')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updatedby', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='cooperationdocumentchoice',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cooperationdocument'),
        ),
        migrations.AlterField(
            model_name='history',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cooperationdocument'),
        ),
        migrations.AlterField(
            model_name='user',
            name='cooperation_document',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.cooperationdocument'),
        ),
        migrations.DeleteModel(
            name='CooperationDucument',
        ),
    ]