from django.db import models

# Create your models here.

class Videos(models.Model):
    nombre = models.CharField(max_length=50, null=False)
    descripcion = models.CharField(max_length=500, null=False)
    miniatura = models.FileField(upload_to='upload/photos')
    video = models.FileField(upload_to='upload/videos')
    categoria = models.CharField(max_length=15, null=False)
