from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Impresora3d, Categoria
from django import forms

class Impresora3dAdminForm(forms.ModelForm):
    latitud = forms.DecimalField(label='Latitud', required=False)
    longitud = forms.DecimalField(label='Longitud', required=False)

    class Meta:
        model = Impresora3d
        fields = '__all__'

@admin.register(Impresora3d)
class Impresora3dAdmin(LeafletGeoAdmin):
    default_lon = -100.0  # Longitud inicial (centro de América)
    default_lat = 30.0  # Latitud inicial (centro de América)
    default_zoom = 4  # Nivel de zoom inicial (zoom moderado)
    list_display = ('nombre', 'ubicacion', 'precio')  # Campos a mostrar en la lista
    form = Impresora3dAdminForm

    # Personalización del formulario
    fieldsets = (
        (None, {
            'fields': ('nombre', 'descripcion', 'imagen', 'categoria', 'ubicacion', 'precio', 'correo', 'telefono', 'impresoras')
        }),
        ('Ubicación Manual', {
            'fields': ('latitud', 'longitud'),
            'classes': ('collapse',),
        }),
    )

    # Sobrescribir el método save para manejar la ubicación
    def save_model(self, request, obj, form, change):
        ubicacion = form.cleaned_data.get('ubicacion')
        latitud = form.cleaned_data.get('latitud')
        longitud = form.cleaned_data.get('longitud')

        if latitud is not None and longitud is not None:
            obj.ubicacion = f'POINT({longitud} {latitud})'

        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['ubicacion'].required = False
        return form

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    pass  # Esto es solo para registrar la categoría sin personalización adicional
