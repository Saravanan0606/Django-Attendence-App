# Generated by Django 4.2.7 on 2024-02-11 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_userprofile_profile_picture_attendance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='recorded_at',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='longitude',
        ),
    ]
