# Generated by Django 5.0.6 on 2024-06-14 17:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0006_rename_files_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='department.department'),
        ),
    ]
