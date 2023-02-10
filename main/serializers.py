import zipfile

from rest_framework import serializers
from .models import *
from FileSharingApp.settings import *


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'


class FileListSerializer(serializers.ModelSerializer):
    file = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False, max_length=10000, use_url=False)
    )
    folder = serializers.CharField(required=False)

    def zip_files(self, folder):
        with zipfile.ZipFile(f'{folder.folder_name}.zip', 'w') as new_zip:
            for file in folder.file_set.all():
                new_zip.write(f'static/{file.file}')

    def create(self, validated_data):
        files = validated_data.get('file')
        folder = validated_data.get('folder')
        file_objs = []
        for file in files:
            file_obj = File.objects.create(file=file, folder=folder)
            file_objs.append(file_obj)
        return (i for i in file_objs)

    class Meta:
        model = File
        fields = ['id', 'file', 'folder', 'created_at']


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
