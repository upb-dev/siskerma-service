# Generated by Django 4.1.3 on 2023-01-10 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_cooperationducument_fakultas_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fakultas',
            name='last_ai_number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fakultas',
            name='last_moa_number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fakultas',
            name='last_mou_number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]