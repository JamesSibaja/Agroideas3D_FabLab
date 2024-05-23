from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from mapa.views import mapa, puntos, obtener_informacion

urlpatterns = [
    path('mapa/',mapa, name='Mapa'),
    path('puntos/',puntos, name='Puntos'),
    path('obtener_informacion/',obtener_informacion, name='obtener_informacion'),
]
