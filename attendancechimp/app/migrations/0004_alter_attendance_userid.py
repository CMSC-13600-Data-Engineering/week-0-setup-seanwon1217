# Generated by Django 4.2.1 on 2023-05-10 13:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_alter_attendance_time_alter_attendance_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='userid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]