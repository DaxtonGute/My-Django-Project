# Generated by Django 3.1.7 on 2021-05-11 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermessage',
            name='Time_Stamp',
            field=models.DateTimeField(),
        ),
    ]