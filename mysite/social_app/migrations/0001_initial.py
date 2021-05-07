# Generated by Django 3.1.7 on 2021-05-07 20:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConvoPreview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Group_Name', models.CharField(default='DEFAULT_GROUP', max_length=200)),
                ('Thumbnail', models.ImageField(default='/404.png', upload_to='uploads/')),
                ('GroupId', models.IntegerField(unique=True)),
                ('Description', models.CharField(default='DEFAULT_DESCRIPTION', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('Message_Text', models.CharField(default='DEFAULT_MESSAGE', max_length=200)),
                ('Time_Stamp', models.DateField()),
                ('MessageId', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Author', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
                ('GroupConvo', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.SET_DEFAULT, to='social_app.convopreview')),
            ],
        ),
        migrations.CreateModel(
            name='Post_Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_app.convopreview')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
