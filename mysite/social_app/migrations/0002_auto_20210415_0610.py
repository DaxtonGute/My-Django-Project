# Generated by Django 3.1.7 on 2021-04-15 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Message',
            new_name='UserMessage',
        ),
    ]
