# Generated by Django 5.0.6 on 2024-06-04 17:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_ipmarkremovalrequest_approved_by_dean_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalfile',
            name='file',
            field=models.FileField(upload_to='files/'),
        ),
        migrations.CreateModel(
            name='IPMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prelim', models.FloatField(blank=True, null=True)),
                ('midterm', models.FloatField(blank=True, null=True)),
                ('semis', models.FloatField(blank=True, null=True)),
                ('finals', models.FloatField(blank=True, null=True)),
                ('final_grade', models.CharField(blank=True, max_length=10, null=True)),
                ('remarks', models.CharField(blank=True, max_length=10, null=True)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.ipmarkremovalrequest')),
            ],
        ),
    ]