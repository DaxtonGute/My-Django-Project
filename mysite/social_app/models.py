from django.db import models
import datetime
from django.utils import timezone
from django.db.models.signals import post_save
from django.contrib.postgres.fields import ArrayField
from django.dispatch import receiver
from django.contrib.auth.models import User
from math import log


class ConvoPreview(models.Model): # These fields will mostly be displayed on the main page as separate group chats
    Group_Name = models.CharField(max_length=200, default="DEFAULT_GROUP")
    Thumbnail = models.ImageField(upload_to ='uploads/', default='/404.png')
    GroupId = models.IntegerField(unique=True)
    Description = models.CharField(max_length=500, default="DEFAULT_DESCRIPTION")
    Time_Stamp = models.DateTimeField()

    def __str__(self): # This gives the name of the object
        groupid = "GROUP ("+str(self.GroupId) +")"
        return groupid

    @property
    def view_count(self): # returns the view count of a given group conversation
        return Post_Likes.objects.filter(post=self).count()

    @property
    def hotness(self): # returns the hotness number of a given group conversation for filtering
        order = log(max(abs(Post_Likes.objects.filter(post=self).count()), 1), 10)
        epoch = datetime.datetime(1970, 1, 1)
        td = self.Time_Stamp.replace(tzinfo=None) - epoch
        epoch_seconds = td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)
        seconds = epoch_seconds - 1134028003
        return round(order + seconds / 45000, 7)

class Post_Likes(models.Model): # This is a like. It requires a reference to both a user and a group chat
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     post = models.ForeignKey(ConvoPreview, on_delete=models.CASCADE)

class UserMessage(models.Model): # This is a user message. These are displayed in the  subpages after clicking off the main page.
    Message_Text = models.CharField(max_length=200, default="DEFAULT_MESSAGE")
    Time_Stamp = models.DateTimeField()
    Author = models.ForeignKey(User, default=-1,  on_delete=models.SET_DEFAULT)
    GroupConvo = models.ForeignKey(ConvoPreview, default=-1,  on_delete=models.SET_DEFAULT)
    MessageId = models.AutoField(primary_key=True, unique=True)

    def __str__(self): # This gives the name of the object
        messageid = "MESSAGE ("+str(self.MessageId) +")"
        return messageid
