# Generated by Django 5.0.6 on 2024-06-05 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_student_avatar_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
