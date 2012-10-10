from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # This is the only required field
    user = models.ForeignKey(User, unique=True)

    # The rest is completely up to you...
    favorite_band = models.CharField(max_length=100, blank=True)
    favorite_cheese = models.CharField(max_length=100, blank=True)
    lucky_number = models.IntegerField()
