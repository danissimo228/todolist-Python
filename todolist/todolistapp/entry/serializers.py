from rest_framework import serializers
from .models import *


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ['id', 'text', 'entry_status']


class EntryAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryAccess
        fields = ['id', 'username', 'entry_access_status']


class EntryLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryLink
        fields = ['entry', 'text', 'url']
