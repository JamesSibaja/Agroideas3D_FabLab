import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agroideas.settings')
from catalogo.models import modelo3d

from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from jsonfield import JSONField
# from django.db import models
from django.contrib.auth.models import User
from colorfield.fields import ColorField
from django.contrib.gis.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=25)
    descripcion= models.CharField(max_length=500)
    color = ColorField(default='#FFFFFF')

    def __str__(self):
        return self.nombre

class Impresora3d(models.Model):
    nombre = models.CharField(max_length=25)
    descripcion= models.CharField(max_length=500)
    imagen = models.ImageField(upload_to='impresoras',null=True,)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    ubicacion = models.PointField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    impresoras = models.CharField(max_length=300)

    def __str__(self):
        return self.nombre


# Create your models here.
# class Project(models.Model):
#     name = models.CharField(max_length=25)
#     description = models.CharField(max_length=500)

#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     adminUsers = models.ManyToManyField(User, related_name='adminUsers')
#     sharedUsers = models.ManyToManyField(User, related_name='sharedUsers')
#     invitedUsers = models.ManyToManyField(User, related_name='invitedUsers')

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse('project-detail', args=[str(self.id),str(0),str(0)])

# class ProjectSlide(models.Model):
#     name = models.CharField(max_length=25)
#     description = models.CharField(max_length=500)
#     adminPermission = models.BooleanField(default=False)


#     slide = models.ForeignKey(modelo3d, on_delete=models.SET_NULL, null=True)
#     project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse('project-slide-detail', args=[str(self.id)])
    

# class Notes(models.Model):
#     name = models.CharField(max_length=50)
    
#     description = models.TextField(max_length=500)
#     geojson_data = models.TextField(null=True, blank=True)
#     show = models.BooleanField()

#     xUnoPos = models.FloatField()
#     yUnoPos = models.FloatField()
#     xDosPos = models.FloatField()
#     yDosPos = models.FloatField()
    
#     project = models.ForeignKey(ProjectSlide, on_delete=models.CASCADE, null=True)

#     def __str__(self):
#         return self.name  

#     def get_absolute_url(self):
#         return reverse('note-detail', args=[str(self.id),str(self.project.id)])
    
# class Message(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     project = models.ForeignKey(Project,  on_delete=models.CASCADE)
#     contenido = models.TextField()
#     fecha_envio = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user}: {self.contenido}"
    
