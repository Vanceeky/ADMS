# Generated by Django 5.0.6 on 2024-06-13 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0003_alter_department_dean'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='logos/'),
        ),
    ]