# Generated by Django 4.1.3 on 2023-05-23 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_alter_cooperationchoice_code_alter_fakultas_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='code',
            field=models.CharField(max_length=10, null=True),
        ),
    ]