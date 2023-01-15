# Generated by Django 4.1.3 on 2022-12-31 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cooperationducument',
            name='responsible_approval_name',
        ),
        migrations.RemoveField(
            model_name='cooperationducument',
            name='responsible_approval_position',
        ),
        migrations.RemoveField(
            model_name='cooperationducument',
            name='responsible_email',
        ),
        migrations.RemoveField(
            model_name='cooperationducument',
            name='responsible_name',
        ),
        migrations.RemoveField(
            model_name='cooperationducument',
            name='responsible_position',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.AddField(
            model_name='user',
            name='responsible_approval_name',
            field=models.CharField(default='', max_length=125),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='responsible_approval_position',
            field=models.CharField(default='position', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='responsible_name',
            field=models.CharField(default='responsible_name', max_length=125),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='responsible_position',
            field=models.CharField(default='responsible+potition', max_length=255),
            preserve_default=False,
        ),
    ]