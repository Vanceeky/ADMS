# Generated by Django 5.0.6 on 2024-06-04 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_ipmark_final_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='ipmark',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
