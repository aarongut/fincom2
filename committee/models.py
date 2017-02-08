from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

class Committee(models.Model):
    name = models.CharField(max_length=100, unique=True)
    chair = models.ForeignKey(User, null=True)

    def __str__(self):
        return self.name
