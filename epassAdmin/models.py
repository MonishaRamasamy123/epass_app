from django.db import models


class AdminUsers(models.Model):
    email_id = models.CharField(max_length=100)
    password = models.CharField(max_length=50)