# Generated by Django 3.1.4 on 2020-12-19 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CSM', '0013_week_unit_unit_caption'),
    ]

    operations = [
        migrations.AddField(
            model_name='week_unit',
            name='abc',
            field=models.CharField(max_length=100, null=True),
        ),
    ]