from django.db import models
from django.conf import settings
from django.db.models import Q
import random

User = settings.AUTH_USER_MODEL

class BarkLike(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    bark = models.ForeignKey("Bark", on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add = True)

class BarkQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(user__username__iexact=username)
    def feed(self, user):
        profiles_exist = user.following.exists()
        followed_users_id = []
        if profiles_exist:
            followed_users_id = user.following.values_list("user__id", flat=True)
        return self.filter(
            Q(user__id__in=followed_users_id) |
            Q(user=user)
            ).distinct().order_by("-timestamp")

class BarkManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return BarkQuerySet(self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user)

class Bark(models.Model):
    # id = models.AutoField(primary_key = True)
    parent = models.ForeignKey("self", null = True, on_delete = models.SET_NULL)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'barks') # Many barks to one user
    content = models.TextField(blank = True, null = True)
    image = models.FileField(upload_to='images/', blank = True, null = True)
    likes = models.ManyToManyField(User, related_name = 'bark_user', blank = True, through = BarkLike)
    timestamp = models.DateTimeField(auto_now_add = True)

    objects = BarkManager()
    # def __str__(self):
    #     return self.content

    class Meta:
        ordering = ['-id']

    @property
    def is_rebark(self):
        return self.parent != None