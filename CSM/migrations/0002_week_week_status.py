# Generated by Django 3.1.4 on 2021-04-18 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CSM', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='week',
            name='week_status',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
