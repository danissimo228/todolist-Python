from django.db import models
from folder.models import Folder
from page.models import Page


class Entry(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    text = models.CharField(null=False)
    entry_status = models.CharField(max_length=11)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    author_user = models.CharField(max_length=20)
    update_user = models.CharField(max_length=20, null=True)
    page = models.ForeignKey(Page, on_delete=models.PROTECT)

    def __str__(self):
        return self.text


class EntryLink(models.Model):
    """Latest version before update Entry"""
    entry = models.OneToOneField(
        Entry,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    text = models.CharField(null=False)
    url = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.text


class EntryAccess(models.Model):
    """Access to Entry"""
    id = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=50)
    entry_access_status = models.CharField(max_length=7)
    folder = models.ForeignKey(Folder, on_delete=models.PROTECT)

    def __str__(self):
        return self.username


class EntryStatus:
    DONE = "done",
    IN_PROCESS = "in_process",
    CANCELED = "canceled"
