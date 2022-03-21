from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from core.utils import validate_contact_number
from django.db import models

class User(AbstractUser):
    
    name = CharField(_("Name of User"), blank=True, max_length=255)
    mobile_number = models.CharField(max_length=11, validators=[validate_contact_number], unique=True, default=None)
    
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
