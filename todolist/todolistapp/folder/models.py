from django.db import models
from users.models import User


class Folder(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=20)
    is_delete = models.BooleanField(default=False)
    status_access = models.BooleanField(null=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False)

    def __str__(self):
        return self.name


class FolderAccess(models.Model):
    """Access for Folder"""
    id = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=50)
    folder = models.ForeignKey(Folder, on_delete=models.PROTECT, null=False)

    def __str__(self):
        return self.username
