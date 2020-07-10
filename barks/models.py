from django.db import models
from django.conf import settings
import random

User = settings.AUTH_USER_MODEL

class BarkLike(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    bark = models.ForeignKey("Bark", on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add = True)

class Bark(models.Model):
    # id = models.AutoField(primary_key = True)
    parent = models.ForeignKey("self", null = True, on_delete = models.SET_NULL)
    user = models.ForeignKey(User, on_delete = models.CASCADE) # Many barks to one user
    content = models.TextField(blank = True, null = True)
    image = models.FileField(upload_to='images/', blank = True, null = True)
    likes = models.ManyToManyField(User, related_name = 'bark_user', blank = True, through = BarkLike)
    timestamp = models.DateTimeField(auto_now_add = True)

    # def __str__(self):
    #     return self.content

    class Meta:
        ordering = ['-id']

    @property
    def is_rebark(self):
        return self.parent != None