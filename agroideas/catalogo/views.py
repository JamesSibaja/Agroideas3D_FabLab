from django.shortcuts import render, redirect
from catalogo.models import modelo3d
from django.views.generic import CreateView
from django.views import generic
from django.template import Template, context
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import  UploadFileForm, SlideForm
from .tasks import convert_to_tiles
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.files.base import ContentFile
import os
import logging

# Configura la configuración de registro según tus necesidades
logger = logging.getLogger('myapp.view') 
# Create your views here.

# class micro(generic.DetailView):
#     template_name = "catalogo/microscopio.html"
#     model = modelo3d

# class microfull(generic.DetailView):
#     template_name = "catalogo/microscopiofull.html"
#     model = modelo3d

def catalogo(request):
    queryset = request.GET.get('buscar')
    # ver = request.GET.get('ver')
    # catalogo = modelo3d.objects.filter( assembled=True)
    catalogo = modelo3d.objects.all()
    if queryset:
        palabras = queryset.split()
        condiciones_busqueda = []

        for palabra in palabras:
            condicion = Q(name__icontains=palabra)
            condicion2 = Q(description__icontains=palabra) 
            condiciones_busqueda.append(condicion)
            condiciones_busqueda.append(condicion2)

        consulta = Q()
        for condicion in condiciones_busqueda:
            consulta |= condicion

        catalogo = modelo3d.objects.filter(consulta)
        
    # paginator = Paginator(catalogo,30)

    paginator = Paginator(catalogo,9)
    
    page = request.GET.get('page')
    catalogo = paginator.get_page(page)

    return render(request,"catalogo/catalogo.html",{'catalogo':catalogo})

# def deleteSlide(request, project_id):
#     instancia = Project.objects.get(id=project_id)
#     new_url = 'project-list'
#     instancia.delete()

#     return redirect(new_url)

# # def upload_file(request):
# #     listSlide = OpenSlide.objects.filter( assembled=False).distinct()


# #     if request.method == 'POST':
# #         option = int(request.POST.get('option'))
# #         if(option == 1):
# #             uploaded_file = request.FILES['file']
# #             name = uploaded_file.name + '_' + str(OpenSlide.objects.count())
# #             instance = OpenSlide(name=name)
# #             instance.save()
# #             instance.path = 'media/archivo/' +str(instance.id) + '_' + uploaded_file.name
# #             instance.save()

# #             os.makedirs('media/archivo/', exist_ok=True)

# #             with open('media/archivo/' +str(instance.id)+ '_' + uploaded_file.name, 'wb') as destino:
# #                 for chunk in uploaded_file.chunks():
# #                     destino.write(chunk)
            
# #             response_data = {'message': 'Archivo cargado exitosamente'}
# #             return JsonResponse(response_data)
        
# #         else:
# #             # logger.info('Hola1')
# #             form = SlideForm(request.POST, request.FILES)
# #             if form.is_valid():
# #                 option = int(request.POST.get('option'))
# #                 rawSlide = OpenSlide.objects.get(id=int(request.POST.get('slide')))
# #                 rawSlide.assembled = True
# #                 rawSlide.save()
# #                 instance = form.save(commit=False)
# #                 instance.save()
# #                 instance.rawSlide = rawSlide
# #                 instance.image = 'slides/slide' +str(instance.id)+'/1/0.jpg'
# #                 instance.path = 'slide' +str(instance.id)
# #                 instance.save()
# #                 logger.info('Hola')

# #                 convert_to_tiles.delay(rawSlide.path,'media/slides/slide' +str(instance.id),instance.rawSlide.id,instance.id)
# #             else:
# #                 return JsonResponse(form.errors, status=400)  # Devuelve errores de validación

# #     else:
# #         form = SlideForm()

# #     return render(request, 'catalogo/subir_archivo.html', {'form':form,'listSlide':listSlide})

# def upload_file(request):
#     listSlide = OpenSlide.objects.filter(assembled=False).distinct()

#     if request.method == 'POST':
#         option = int(request.POST.get('option'))
#         if option == 1:
#             uploaded_file = request.FILES['file']
#             name = uploaded_file.name + '_' + str(OpenSlide.objects.count())
#             instance = OpenSlide(name=name)
#             instance.save()

#             file_content = b''
#             for chunk in uploaded_file.chunks():
#                 file_content += chunk

#             instance.file_field.save(uploaded_file.name, ContentFile(file_content))
#             instance.save()

#             response_data = {'message': 'Archivo cargado exitosamente'}
#             return JsonResponse(response_data)

#         else:
#             form = SlideForm(request.POST, request.FILES)
#             if form.is_valid():
#                 rawSlide = OpenSlide.objects.get(id=int(request.POST.get('slide')))
#                 rawSlide.assembled = True
#                 rawSlide.save()
#                 instance = form.save(commit=False)
#                 instance.rawSlide = rawSlide
#                 instance.image = 'slides/slide' + str(instance.id) + '/1/0.jpg'
#                 instance.path = 'slide' + str(instance.id)
#                 instance.save()

#                 convert_to_tiles.delay(rawSlide.path, 'media/slides/slide' + str(instance.id), instance.rawSlide.id, instance.id)
#             else:
#                 return JsonResponse(form.errors, status=400)  

#     else:
#         form = SlideForm()

#     return render(request, 'catalogo/subir_archivo.html', {'form':form, 'listSlide':listSlide})

# def processing(request):
#     listSlide = modelo3d.objects.filter(assembled=False,error=False).distinct()
#     listmodelo3dError = modelo3d.objects.filter(error=True).distinct()

#     # if request.method == 'POST':
#     #     option = int(request.POST.get('option'))
#     #     if(option == 1):
#     #         uploaded_file = request.FILES['file']
#     #         name = uploaded_file.name + '_' + str(OpenSlide.objects.count())
#     #         instance = OpenSlide(name=name)
#     #         instance.save()
#     #         instance.path = 'media/archivo/' +str(instance.id) + '_' + uploaded_file.name
#     #         instance.save()

#     #         os.makedirs('media/archivo/', exist_ok=True)

#     #         with open('media/archivo/' +str(instance.id)+ '_' + uploaded_file.name, 'wb') as destino:
#     #             for chunk in uploaded_file.chunks():
#     #                 destino.write(chunk)
            
#     #         response_data = {'message': 'Archivo cargado y procesado exitosamente'}
#     #         return JsonResponse(response_data)
        
#     #     else:
#     #         logger.info('Hola1')
#     #         form = SlideForm(request.POST, request.FILES)
#     #         if form.is_valid():
#     #             option = int(request.POST.get('option'))
#     #             rawSlide = OpenSlide.objects.get(id=int(request.POST.get('slide')))
#     #             instance = form.save(commit=False)
#     #             instance.save()
#     #             instance.rawSlide = rawSlide
#     #             instance.image = 'slides/slide' +str(instance.id)+'/1/0.jpg'
#     #             instance.path = 'slide' +str(instance.id)
#     #             instance.save()
#     #             logger.info('Hola')

#     #             convert_to_tiles.delay(rawSlide.path,'media/slides/slide' +str(instance.id),instance.rawSlide.id,instance.id)
#     #         else:
#     #             return JsonResponse(form.errors, status=400)  # Devuelve errores de validación

#     # else:
#     #     form = SlideForm()

#     return render(request, 'catalogo/procesando.html', {'listSlide':listSlide,'listSlideError':listSlideError})

def delete(request, modelo3d_id):
    instancia = modelo3d.objects.get(id=modelo3d_id)
    new_url = '/processing/'
    instancia.delete()

    return redirect(new_url)