from django.db import models

# Create your models here.

class Videos(models.Model):
    nombre = models.CharField(max_length=50, null=False)
    descripcion = models.CharField(max_length=250, null=False)
    miniatura = models.ImageField(upload_to='')
    categoria = models.CharField(max_length=15, null=False)
