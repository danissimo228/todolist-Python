from django.contrib import admin
from .models import Folder, FolderAccess


admin.site.register(Folder)
admin.site.register(FolderAccess)
