from rest_framework import serializers
from .models import Folder, FolderAccess


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name', 'status_access']


class FolderAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderAccess
        fields = ['id', 'username']
