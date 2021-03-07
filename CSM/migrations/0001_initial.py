# Generated by Django 3.1.6 on 2021-03-07 15:21

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('modified', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('title', models.CharField(max_length=50)),
                ('tagline', models.CharField(max_length=50)),
                ('short_description', models.CharField(max_length=100)),
                ('course_image', models.ImageField(blank=True, null=True, upload_to='csm_images/')),
                ('video_page_image', models.ImageField(blank=True, null=True, upload_to='csm_images/')),
                ('instructor', models.CharField(blank=True, max_length=200, null=True)),
                ('trainee_name', models.CharField(blank=True, max_length=64)),
                ('trainee_bio', models.TextField(blank=True)),
                ('course_points', models.IntegerField(default=0)),
                ('xp_points_perq', models.IntegerField(default=0)),
                ('certificate', models.FileField(null=True, upload_to='csm_certificates/')),
                ('requirements', models.TextField(blank=True)),
                ('learnings', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_private', models.CharField(max_length=100, null=True)),
                ('week_name', models.CharField(max_length=100)),
                ('week_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('week_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CSM.course')),
            ],
        ),
        migrations.CreateModel(
            name='Week_Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_caption', models.CharField(max_length=500, null=True)),
                ('unit_video1', models.FileField(null=True, upload_to='Week_Videos/')),
                ('unit_video2', models.FileField(null=True, upload_to='Week_Videos/')),
                ('unit_video3', models.FileField(null=True, upload_to='Week_Videos/')),
                ('u_capThree', models.CharField(blank=True, max_length=100, null=True)),
                ('uCapOne', models.CharField(blank=True, max_length=150, null=True)),
                ('uCap2', models.CharField(blank=True, max_length=150, null=True)),
                ('video1_duration', models.TimeField(null=True)),
                ('video2_duration', models.TimeField(null=True)),
                ('video3_duration', models.TimeField(null=True)),
                ('unit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CSM.week')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', jsonfield.fields.JSONField()),
                ('score', models.CharField(max_length=100)),
                ('timetaken', models.CharField(max_length=100, null=True)),
                ('user_answer', jsonfield.fields.JSONField()),
                ('auth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'results',
            },
        ),
        migrations.CreateModel(
            name='Quizz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ques_no', models.IntegerField(null=True)),
                ('question', models.CharField(max_length=250)),
                ('option1', models.CharField(max_length=100)),
                ('option2', models.CharField(max_length=100)),
                ('option3', models.CharField(max_length=100)),
                ('option4', models.CharField(max_length=100)),
                ('option', jsonfield.fields.JSONField(null=True)),
                ('answer', models.CharField(max_length=100)),
                ('option_available', models.BooleanField(default=False, null=True)),
                ('course_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CSM.course')),
                ('week_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CSM.week')),
            ],
        ),
        migrations.CreateModel(
            name='CreateCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_category', models.CharField(max_length=255, null=True)),
                ('create_sub', models.CharField(max_length=255, null=True)),
                ('create_course', models.CharField(max_length=255)),
                ('create_time', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('create_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CSM.createcourse'),
        ),
        migrations.AddField(
            model_name='course',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
