# Generated by Django 5.0.6 on 2024-06-13 19:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_courseguide_status'),
        ('department', '0003_alter_department_dean'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseguide',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='department.department'),
        ),
    ]
