# Generated by Django 3.1.6 on 2021-02-10 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CSM', '0030_merge_20210204_1039'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='meta_description',
            new_name='trainee_bio',
        ),
        migrations.RemoveField(
            model_name='course',
            name='meta_keywords',
        ),
        migrations.RemoveField(
            model_name='course',
            name='xp_points',
        ),
        migrations.AddField(
            model_name='course',
            name='trainee_name',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name='course',
            name='video_page_image',
            field=models.ImageField(blank=True, null=True, upload_to='csm_images/'),
        ),
    ]
