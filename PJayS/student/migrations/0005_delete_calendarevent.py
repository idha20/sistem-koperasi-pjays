# Generated by Django 5.1.1 on 2024-11-02 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_calendarevent_description_alter_calendarevent_member'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CalendarEvent',
        ),
    ]
