# Generated by Django 4.2.3 on 2023-07-19 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folder', '0002_folder_is_delete'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PageAccess',
        ),
    ]