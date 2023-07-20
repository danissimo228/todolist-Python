# Generated by Django 4.2.3 on 2023-07-19 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('folder', '0003_delete_pageaccess'),
        ('page', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='status_access',
        ),
        migrations.CreateModel(
            name='PageAccess',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(max_length=50)),
                ('page_access_status', models.CharField(max_length=7)),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='folder.folder')),
            ],
        ),
    ]
