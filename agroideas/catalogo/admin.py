from django.contrib import admin
from .models import modelo3d,OpenSlide

# Register your models here.
# class SlideAdmin(admin.ModelAdmin):
    

admin.site.register(modelo3d)
admin.site.register(OpenSlide)