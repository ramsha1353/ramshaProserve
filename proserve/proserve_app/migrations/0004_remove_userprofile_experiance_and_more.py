# Generated by Django 4.2.3 on 2023-08-11 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proserve_app', '0003_remove_workerprofile_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='experiance',
        ),
        migrations.AddField(
            model_name='workerprofile',
            name='experiance',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
