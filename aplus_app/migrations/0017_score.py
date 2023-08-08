# Generated by Django 4.1.7 on 2023-08-08 00:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aplus_app', '0016_alter_room_qrcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplus_app.room')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplus_app.student')),
            ],
        ),
    ]
