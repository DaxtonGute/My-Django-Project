# Generated by Django 3.1.7 on 2021-05-07 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0002_convopreview_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convopreview',
            name='GroupId',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, unique=True),
        ),
    ]
