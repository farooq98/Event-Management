from django.db import models
from django.conf import settings
# Create your models here.

class Event(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="events", on_delete=models.PROTECT)
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="events_attended")

    def __str__(self):
        return self.title