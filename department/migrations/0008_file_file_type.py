# Generated by Django 4.2.9 on 2024-06-25 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0007_file_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file_type',
            field=models.CharField(blank=True, max_length=155, null=True),
        ),
    ]