# Generated by Django 4.2.3 on 2023-07-20 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folder', '0003_delete_pageaccess'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EntryAccess',
        ),
    ]
