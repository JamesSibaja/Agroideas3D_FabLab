from django.shortcuts import get_object_or_404,render, redirect              
from django.views.generic import CreateView
from django.views import generic
from django.template import Template, context
from django.views.generic.edit import FormView, DeleteView
from django.db.models import Q
from mapa.models import Impresora3d
from catalogo.models import modelo3d
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.http import HttpResponse

def obtener_informacion(request):
    if request.method == 'GET':
        impresora_id = request.GET.get('id')
        try:
            impresora = Impresora3d.objects.get(id=impresora_id)
            # Supongamos que quieres devolver algunos datos de la impresora
            data = {
                'nombre': impresora.nombre,
                'descripcion': impresora.descripcion,
                'imagen':impresora.imagen.url,
                # Agrega otros campos que quieras devolver
            }
            return JsonResponse(data)
        except Impresora3d.DoesNotExist:
            return JsonResponse({'error': 'Impresora no encontrada'}, status=404)


def mapa(request):    
    return render(request,"mapa/mapa.html")

def puntos(request):
    impresoras = Impresora3d.objects.all()
    data = []
    for impresora in impresoras:
        data.append({
            'nombre': impresora.nombre,
            'id': impresora.id,
            'latitud': impresora.ubicacion.y,
            'longitud': impresora.ubicacion.x,
            'precio': impresora.precio,
            'categoria': impresora.categoria.nombre,
            'color': impresora.categoria.color,
        })
    return JsonResponse(data, safe=False)