from django.db import models
from folder.models import Folder


class Page(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=20)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    author_user = models.CharField(max_length=20)
    update_user = models.CharField(max_length=20, null=True)
    folder = models.ForeignKey(Folder, on_delete=models.PROTECT, null=False)

    def __str__(self):
        return self.name


class PageAccess(models.Model):
    """Access for page"""
    id = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=50)
    page_access_status = models.CharField(max_length=7)
    folder = models.ForeignKey(Folder, on_delete=models.PROTECT)

    def __str__(self):
        return self.username


class StatusAccess:
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    CREATE = "create"
