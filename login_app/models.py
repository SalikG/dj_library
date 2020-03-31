from secrets import token_urlsafe
from django.contrib.auth.models import User
from datetime import datetime
from django.db import models


class Role(models.Model):
    role = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.role}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.user} - {self.role}'


class PasswordResetRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=43, default=token_urlsafe)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.created_timestamp}'
