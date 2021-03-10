from django.db import models
import datetime
from django.utils import timezone

class YourMessage(models.Model):
    Message_Text = models.CharField(max_length=200)

    def __str__(self):
        return self.Message_Text


class MyMessage(models.Model):
    Message_Text = models.CharField(max_length=200)

    def __str__(self):
        return self.Message_Text

class ConvoPreview(models.Model):
    Message_Text = models.CharField(max_length=200)

    def __str__(self):
        return self.Message_Text
