from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Usuario(AbstractUser):
    temp_password = models.CharField(max_length=8)

    def __str__(self):
        return self.username

class Videos(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.CharField(max_length=1000, null=False)
    miniatura = models.FileField(upload_to='upload/photos')
    video = models.FileField(upload_to='upload/videos')
    visitas = models.IntegerField()
