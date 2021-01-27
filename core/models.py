from django.db import models
from django.contrib.auth.models import User


class Request(models.Model):
    REQUEST_STATUS = [
        ('A', 'Approved'),
        ('R', 'Rejected')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    checked = models.BooleanField(default=False)
    status = models.CharField(
        max_length=1, choices=REQUEST_STATUS, blank=True)
    
    def __str__(self):
        return self.user.username

    @property
    def name(self):
        return self.user.username
