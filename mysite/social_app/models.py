from django.db import models
import datetime
from django.utils import timezone

class UserMessage(models.Model):
    Message_Text = models.CharField(max_length=200, default="DEFAULT_MESSAGE")
    Time_Stamp = models.DateField()
    Author = models.CharField(max_length=200, default="DEFAULT_AUTHRO")
#    Belongs_To = models.ConvoPreview

    def __str__(self):
        return self.Message_Text

class ConvoPreview(models.Model):
    Group_Name = models.CharField(max_length=200, default="DEFAULT_GROUP")
    Thumbnail = models.ImageField(upload_to ='uploads/', default='/404.png')

    def __str__(self):
        return self.Group_Name
