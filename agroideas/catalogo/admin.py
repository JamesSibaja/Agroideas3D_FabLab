from django.contrib import admin
from .models import modelo3d, materiales, categoria_catalogo, medida

# Register your models here.
# class SlideAdmin(admin.ModelAdmin):
    

admin.site.register(modelo3d)
admin.site.register(materiales)
admin.site.register(categoria_catalogo)
admin.site.register(medida)

