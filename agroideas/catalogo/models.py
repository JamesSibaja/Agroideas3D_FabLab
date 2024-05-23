import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agroideas.settings')
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
# class OpenSlide(models.Model):
#     name = models.CharField(unique=True, max_length=50)
#     path = models.CharField(max_length=50,null=True)
#     file = models.FileField(max_length=50,null=True)
#     assembled = models.BooleanField(default=False)

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse('open-micro-slide', args=[str(self.id)])
class materiales(models.Model):
    nombre = models.CharField(unique=True, max_length=50)
    descripcion = models.CharField(max_length=300)
    def __str__(self):
        return self.nombre

class categoria_catalogo(models.Model):
    nombre = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=300)
    def __str__(self):
        return self.nombre

class modelo3d(models.Model):
    nombre = models.CharField(unique=True, max_length=50)
    descripcion = models.CharField(max_length=2000)
    # assembled = models.BooleanField(default=False)
    stl = models.FileField(upload_to="archivo")
    imagen = models.ImageField(upload_to='modelos',null=True)
    categoria = models.ForeignKey(categoria_catalogo, on_delete=models.SET_NULL, null=True)
    material = models.ForeignKey(materiales, on_delete=models.SET_NULL, null=True)
    calidad = models.CharField( max_length=50)
    descripcion_corta  = models.CharField( max_length=150)
    soportes = models.BooleanField(default=False,null=True)
    horas = models.IntegerField(default=0)
    minutos = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('modelo-3d', args=[str(self.id)])

    # def getAbsoluteUrl(self):
    #     return reverse('micro-slide-full', args=[str(self.id)])

class medida(models.Model):
    nombre = models.CharField(unique=True, max_length=50)
    descripcion = models.CharField(max_length=200)
    modelo = models.ForeignKey(modelo3d, on_delete=models.SET_NULL, null=True)
    medida = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.nombre


