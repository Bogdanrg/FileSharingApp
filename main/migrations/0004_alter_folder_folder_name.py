# Generated by Django 4.0.6 on 2022-07-28 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_folder_folder_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='folder_name',
            field=models.CharField(blank=True, default='Untitled', max_length=250, null=True),
        ),
    ]