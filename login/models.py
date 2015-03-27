from django.db import models


class LoginToken(models.Model):
    token_id = models.CharField(max_length=50)


class LoginRequest(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
# Create your models here.
