from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.TextField(max_length=50)
    phone = models.BigIntegerField()
    message1 = models.TextField(max_length=1000)
    message2 = models.TextField(max_length=1000)
    message3 = models.TextField(max_length=1000)
    message4 = models.TextField(max_length=1000)