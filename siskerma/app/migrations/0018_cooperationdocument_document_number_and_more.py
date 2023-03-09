# Generated by Django 4.1.3 on 2023-03-09 05:58

from django.db import migrations, models
import siskerma.app.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_cooperationevidence_remove_workerfcmtoken_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cooperationdocument',
            name='document_number',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='cooperationdocument',
            name='number',
            field=models.IntegerField(default=siskerma.app.models.next_number),
        ),
    ]