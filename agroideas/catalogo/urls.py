from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from catalogo.views import catalogo, delete
from . import views
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

def admin_required(view_func):
    """
    Decorador que restringe el acceso a administradores.
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Acceso denegado. Debes ser administrador para acceder a esta página.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view



urlpatterns = [
    path('', catalogo, name = "Inicio"),
    # path('micro/<pk>/',micro.as_view(),name='micro-slide'),

    
    # path('upload_file/', admin_required(views.upload_file), name='upload_file'),
    # path('processing/', admin_required(views.processing), name='processing'),
    # # path('deleteSlide/<int:slide_id>', deleteSlide),
    # path('delete/<int:slide_id>', admin_required(delete))
]
