# Generated by Django 3.1.7 on 2021-04-30 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0003_auto_20210429_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwrapper',
            name='starredGroupConvos',
            field=models.ManyToManyField(blank=True, null=True, to='social_app.ConvoPreview'),
        ),
    ]
