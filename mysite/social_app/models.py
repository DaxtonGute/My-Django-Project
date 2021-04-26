from django.db import models
import datetime
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class UserProfile(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    password = models.CharField(max_length=150)

    def __str__(self):
        return self.username


# @receiver(post_save, sender=UserProfile)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#     instance.UserProfile.save()

class ConvoPreview(models.Model):
    Group_Name = models.CharField(max_length=200, default="DEFAULT_GROUP")
    Thumbnail = models.ImageField(upload_to ='uploads/', default='/404.png')
    GroupId = models.AutoField(primary_key=True, unique=True)
    GroupIdInt = str(GroupId)

    def __str__(self):
        groupid = "GROUP ("+str(self.GroupId) +")"
        return groupid

class UserMessage(models.Model):
    Message_Text = models.CharField(max_length=200, default="DEFAULT_MESSAGE")
    Time_Stamp = models.DateField()
    Author = models.ForeignKey(User, default=-1,  on_delete=models.SET_DEFAULT)
    GroupConvo = models.ForeignKey(ConvoPreview, default=-1,  on_delete=models.SET_DEFAULT)
    MessageId = models.AutoField(primary_key=True, unique=True)
    #objects = UserMessageManager

    def __str__(self):
        messageid = "MESSAGE ("+str(self.MessageId) +")"
        return messageid

    # def __init__(self, *args):
    #     self.Message_Text=args[0]
    #     self.Time_Stamp=args[1]
    #     self.Author=args[2]
    #     print(ConvoPreview.objects.all())
    #     #ConvoObjext = ConvoPreview.objects.all()[int(args[3])]
    #     for Convo in ConvoPreview.objects.all():
    #         if Convo.Group_Name == args[3]:
    #             self.GroupConvo= ConvoObject

# class UserMessageManager(models.Manager):
#     def create_message(self, title):
#         book = self.create(title=title)
#         # do something with the book
#         return book
