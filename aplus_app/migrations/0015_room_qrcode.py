# Generated by Django 4.1.7 on 2023-08-05 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplus_app', '0014_alter_room_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='qrcode',
            field=models.ImageField(default='qrcodes/default', upload_to='qrcodes'),
        ),
    ]
