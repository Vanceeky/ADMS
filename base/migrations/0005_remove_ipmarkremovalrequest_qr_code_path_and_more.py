# Generated by Django 5.0.6 on 2024-06-02 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_remove_ipmarkremovalrequest_qr_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ipmarkremovalrequest',
            name='qr_code_path',
        ),
        migrations.AddField(
            model_name='ipmarkremovalrequest',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qrcodes/'),
        ),
        migrations.AlterField(
            model_name='ipmarkremovalrequest',
            name='approved_by_ACAD',
            field=models.BooleanField(default=True),
        ),
    ]
