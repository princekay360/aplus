# Generated by Django 4.1.7 on 2023-08-02 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplus_app', '0009_remove_course_registered_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='registered_students',
            field=models.JSONField(default={'data': []}),
        ),
    ]
