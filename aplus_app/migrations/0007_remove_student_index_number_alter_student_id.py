# Generated by Django 4.1.7 on 2023-08-02 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplus_app', '0006_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='index_number',
        ),
        migrations.AlterField(
            model_name='student',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
