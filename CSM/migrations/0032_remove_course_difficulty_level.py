# Generated by Django 3.1.6 on 2021-02-10 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CSM', '0031_auto_20210210_1029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='difficulty_level',
        ),
    ]
