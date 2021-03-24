from django.db import models
import datetime
from django.utils import timezone

class YourMessage(models.Model):
    Message_Text = models.CharField(max_length=200)
    Time_Stamp = models.DateField()

    def __str__(self):
        return self.Message_Text
        return self.Time_Stamp


class MyMessage(models.Model):
    Message_Text = models.CharField(max_length=200)
    Time_Stamp = models.DateField()

    def __str__(self):
        return self.Message_Text
        return self.Time_Stamp

class ConvoPreview(models.Model):
    Message_Text = models.CharField(max_length=200)
    Group_Name = models.CharField(max_length=200)

    def __str__(self):
        return self.Message_Text
        return self.Group_Name
