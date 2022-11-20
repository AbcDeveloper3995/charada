import datetime

from django import template

from apps.charada.models import Configuracion, Contabilidad
from apps.usuario.models import Usuario

register = template.Library()


# FILTRO PARA TOPE BOLA.
@register.filter(name='topeBola')
def topeBola(user):
    tope = Configuracion.objects.all().values('topeBola')
    return tope[0]['topeBola']

# FILTRO PARA TOPE CENTENA PARLET.
@register.filter(name='topeCP')
def topeCP(user):
    tope = Configuracion.objects.all().values('topeCentena')
    return tope[0]['topeCentena']

# FILTRO PARA OBTENER GANACIA DEL DIA.
@register.filter(name='obtenerGanacia')
def obtenerGanacia(limpio, premio):
    ganacia = limpio - premio
    return ganacia

# FILTRO PARA OBTENER LIMPIO DEL DIA.
@register.filter(name='obtenerLimpio')
def obtenerLimpio(user):
    limpio = 0
    fecha = datetime.datetime.today()
    try:
        query = Contabilidad.objects.filter(fecha__day=fecha.date().day)
        for i in query:
            limpio += i.limpio
        return limpio
    except Exception as e:
        print(e)
        query = False
        return query
# FILTRO PARA OBTENER PREMIO DEL DIA.
@register.filter(name='obtenerPremio')
def obtenerPremio(user):
    premio = 0
    fecha = datetime.datetime.today()
    try:
        query = Contabilidad.objects.filter(fecha__day=fecha.date().day)
        for i in query:
            premio += i.premio
        return premio
    except Exception as e:
        print(e)
        query = False
        return query

# FILTRO PARA OBTENER GANACIA DEL DIA.
@register.filter(name='obtenerGananciaGeneral')
def obtenerGananciaGeneral(user):
    premio = 0
    limpio = 0
    ganancia = 0
    fecha = datetime.datetime.today()
    try:
        query = Contabilidad.objects.filter(fecha__day=fecha.date().day)
        for i in query:
            premio += i.premio
            limpio += i.limpio
        ganancia = limpio-premio
        return ganancia
    except Exception as e:
        print(e)
        query = False
        return query

