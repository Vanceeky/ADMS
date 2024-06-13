# Generated by Django 5.0.6 on 2024-06-13 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_courseguide'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseguide',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=50),
        ),
    ]
