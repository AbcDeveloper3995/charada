from django.urls import path
from apps.charada.views import *

app_name = 'charada'

urlpatterns = [
    path('home/', homeView.as_view(), name='home'),

    # JUGADAS
    path('listarJugadas', listarJugadasView.as_view(), name='listarJugadas'),
    path('deleteJugada/<int:pk>', deleteJugadaView.as_view(), name='deleteJugada'),

    # TIROS
    path('listarTiros', listarTirosView.as_view(), name='listarTiros'),
    path('crearTiros', crearTirosView.as_view(), name='crearTiros'),
    path('deleteTiro/<int:pk>', deleteTiroView.as_view(), name='deleteTiro'),

    # CONTABILIDAD
    path('listarContabilidad', listarContabilidadView.as_view(), name='listarContabilidad'),

    # CONFIGURACION
    path('cofiguracion', configuracionView.as_view(), name='cofiguracion'),
    path('tope', topeView.as_view(), name='tope'),

    #FECH
    path('enviandoJugadas', jugadasEnviadasView.as_view(), name='enviandoJugadas'),
    path('reporteGanacia', reporteGanaciaView.as_view(), name='reporteGanacia'),
    path('getLimitados', getLimitadosView.as_view(), name='getLimitados'),
    path('deleteLimitado/<str:pk>', deleteLimitadoView.as_view(), name='deleteLimitado'),
]
