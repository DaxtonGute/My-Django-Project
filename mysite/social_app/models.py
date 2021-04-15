from django.db import models
import datetime
from django.utils import timezone

class UserMessage(models.Model):
    Message_Text = models.CharField(max_length=200)
    Time_Stamp = models.DateField()
    Author = models.CharField(max_length=200)
#    Belongs_To = models.ConvoPreview

    def __str__(self):
        return self.Message_Text

class ConvoPreview(models.Model):
    Group_Name = models.CharField(max_length=200)
    Thumbnail = models.ImageField(upload_to ='uploads/')

    def __str__(self):
        return self.Group_Name
