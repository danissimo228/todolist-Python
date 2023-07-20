from rest_framework import serializers
from .models import *


class PageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'name']


class PageAccessSerializers(serializers.ModelSerializer):
    class Meta:
        model = PageAccess
        fields = ['id', 'username', 'page_access_status']
