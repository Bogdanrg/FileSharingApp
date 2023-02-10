import uuid as uuid
from django.db import models, connection
from django.urls import reverse, reverse_lazy


class Folder(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    folder_name = models.CharField(max_length=250, blank=True, default='Untitled', null=True)
    created_at = models.DateField(auto_now=True)


def user_directory_path(instance, filename):
    return f'photos/{instance.folder.folder_name}/{filename}'


class File(models.Model):
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        path_str = str(self.file)
        return path_str.split("/")[-1]

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE File RESTART IDENTITY;')
