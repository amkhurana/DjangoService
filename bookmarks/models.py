from django.db import models
from django.db.models import CharField, DateTimeField, TextField, ForeignKey
from datetime import datetime
from localusers.models import LocalUser
# Create your models here.

class Bookmark(models.Model):
    user = models.ForeignKey(LocalUser, related_name='bookmarks', on_delete=models.CASCADE)
    latitude = models.CharField(max_length=40)
    longitude = models.CharField(max_length=40)
    timestamp = models.DateTimeField(default=datetime.now())
    #timestamp = DateTimeField(auto_now_add=True)
