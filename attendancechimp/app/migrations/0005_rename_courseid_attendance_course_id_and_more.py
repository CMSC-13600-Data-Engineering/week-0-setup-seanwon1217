# Generated by Django 4.1.7 on 2023-04-24 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_course_meeting_days_course_students'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='courseid',
            new_name='course_id',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='courseid',
            new_name='course_id',
        ),
        migrations.RenameField(
            model_name='in_course',
            old_name='courseid',
            new_name='course_id',
        ),
    ]