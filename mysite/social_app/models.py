from django.db import models
import datetime
from django.utils import timezone

class ConvoPreview(models.Model):
    Group_Name = models.CharField(max_length=200, default="DEFAULT_GROUP")
    Thumbnail = models.ImageField(upload_to ='uploads/', default='/404.png')
    GroupId = models.AutoField(primary_key=True, unique=True)

    def __str__(self):
        groupid = "GROUP ("+str(self.GroupId) +")"
        return groupid

class UserMessage(models.Model):
    Message_Text = models.CharField(max_length=200, default="DEFAULT_MESSAGE")
    Time_Stamp = models.DateField()
    Author = models.CharField(max_length=200, default="DEFAULT_AUTHOR")
    GroupConvo = models.ForeignKey(ConvoPreview, default=-1,  on_delete=models.SET_DEFAULT)
    MessageId = models.AutoField(primary_key=True, unique=True)

    def __str__(self):
        messageid = "MESSAGE ("+str(self.MessageId) +")"
        return messageid

    def __init__(self, args):
        self.Message_Text=args['Message']
        self.Time_Stamp=args['Date']
        self.Author=args['Author']
        self.GroupConvo=args['Convo']
