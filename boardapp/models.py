from django.conf import settings
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.utils import timezone


class Album(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, )
    description = models.TextField()
    publish_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title


class UserProfile(AbstractUser):
    albums = models.ManyToManyField(Album)
    currentAlbum = models.IntegerField(null=True)


def udp(instance, filename):
    return 'images/{0}/{1}'.format(instance.user.username, filename)


class Media(models.Model):
    active = models.BooleanField()
    order = models.IntegerField()
    type = models.CharField(max_length=3)  # pic or vid
    title = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, )
    content = models.FileField(upload_to=udp)
    album = models.ForeignKey(Album)
    caption = models.TextField()
    location = models.CharField(max_length=128)

    def __str__(self):
        return self.title
