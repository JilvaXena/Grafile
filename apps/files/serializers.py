from rest_framework import serializers
from .models import File, Group, ModFiles

class GroupSerializer(serializers.ModelSerializer):
    user_created = serializers.ReadOnlyField(source='user_created.username')
    
    class Meta:
        model = Group
        fields = ['group_id', 'group_name', 'group_text', 'date_created', 'user_created']
        read_only_fields = ['group_id', 'date_created', 'user_created']


class ModFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModFiles
        fields = ['id', 'file', 'index', 'file_hash', 'date_update', 'user_update']
        read_only_fields = ['index', 'date_update', 'user_update']


class FileSerializer(serializers.ModelSerializer):
    user_created = serializers.ReadOnlyField(source='user_created.username')
    
    class Meta:
        model = File
        fields = ['file_id', 'group', 'user_created', 'date_created', 'path']
        # Read only the fields that must NOT be send in the JSON, which are generated in the server
        read_only_fields = ['file_id', 'date_created', 'user_created']