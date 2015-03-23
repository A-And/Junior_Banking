from django.db import models

class login_token(models.Model):
    token_id = models.CharField(max_length=50)

# Create your models here.
