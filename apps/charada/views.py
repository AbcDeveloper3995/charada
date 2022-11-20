import datetime
import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, CreateView

from apps.charada.forms import limitadoForm, tiroForm
from apps.charada.models import *
from apps.utils import definirAMoPM, horarioTarde, horarioNoche


class homeView(LoginRequiredMixin, TemplateView):
    template_name = 'charada/home.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('usuario:login')
        if request.user.fechaCaducidad != None and request.user.fechaCaducidad < datetime.datetime.today().date():
            messages.error(self.request, 'Su sesión ha caducado. Contacte al administrador')
            return redirect('usuario:logout')
        else:
            if definirAMoPM() == 'AM' and horarioTarde():
                print('horario de la tarde')
                return super().dispatch(request, *args, **kwargs)
            elif definirAMoPM() == 'PM' and horarioNoche():
                print('horario de la noche')
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(self.request, 'El sistema esta cerrado en este momento.')
                return redirect('usuario:logout')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tituloPestaña'] = 'SGPC | Home'
        context['configuracion'] = Configuracion.objects.first()
        return context

# PROCEDIMIENTO PARA LISTAR JUGADAS.
class listarJugadasView(LoginRequiredMixin, ListView):
    template_name = 'charada/listar/jugadas.html'
    model = Jugada

    def get_queryset(self):
        fecha = datetime.datetime.today()
        if self.request.user.has_perm('usuario.administrador') or self.request.user.has_perm('usuario.banco'):
            return Jugada.objects.filter(fecha__day=fecha.date().day)
        return Jugada.objects.filter(fecha__day=fecha.date().day, fk_usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jugadas'] = self.get_queryset()
        context['titulo'] = 'Listado de Jugadas'
        context['tituloPestaña'] = 'ABC | Jugadas'
        return context

# PROCEDIMIENTO PARA ELIMINAR JUGADA.
class deleteJugadaView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        data = {}
        try:
            query = get_object_or_404(Jugada, id=self.kwargs['pk'])
            messages.success(self.request, 'La jugada se ha eliminado correctamente.')
            data['url'] = 'http://127.0.0.1:8000/charada/listarJugadas'
            query.delete()
        except Exception as e:
            messages.error(self.request, e)
            data['error'] = 'Ha ocurrido un error'
            data['url'] = 'http://127.0.0.1:8000/charada/listarJugadas'
        return JsonResponse(data, safe=False)

# PROCEDIMIENTO PARA LISTAR LIMITADOS.
class listarLimitadosView(LoginRequiredMixin, ListView):
    template_name = 'charada/listar/limitados.html'
    model = Limitado

    def get_queryset(self):
        return Limitado.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['limitados'] = self.get_queryset()
        context['titulo'] = 'Listado de Limitados'
        context['tituloPestaña'] = 'ABC | Limitados'
        return context

# PROCEDIMIENTO PARA LISTAR CONTABILIDAD.
class listarContabilidadView(LoginRequiredMixin, ListView):
    template_name = 'charada/listar/contabilidad.html'
    model = Contabilidad

    def get_queryset(self):
        return Contabilidad.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contabilidad'] = self.get_queryset()
        context['titulo'] = 'Listado de Contabilidad'
        context['tituloPestaña'] = 'ABC | Contabilidad'
        return context

# COFIGURACION.
class configuracionView(LoginRequiredMixin, TemplateView):
    template_name = 'charada/configuracion.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Limitado.objects.all().values('numero')

    def validarNumeroVacio(self, numero):
        if numero == '':
            return 'numeroVacio'

    def validarTipoVacio(self, tipo):
        if tipo == '':
            return 'tipoVacio'

    def validarFormatoParlet(self, numero):
        if len(numero) != 5:
            return 'errorFormatoParlet'

    def validarFormatoFC(self, numero):
        if len(numero) != 2:
            return 'errorFormatoFC'


    def post(self, request, *args, **kwargs):
        data = {}
        if self.validarNumeroVacio(request.POST['numero']) == 'numeroVacio':
            data['error'] = 'Campo numero es obligatorio.'
            return JsonResponse(data, safe=False)

        if self.validarTipoVacio(request.POST['tipo']) == 'tipoVacio':
            data['error'] = 'Campo tipo es obligatorio.'
            return JsonResponse(data, safe=False)

        action = request.POST['action']
        numero = request.POST['numero']
        tipo = int(request.POST['tipo'])
        precio = int(request.POST['precio'])


        if '-' in numero:
            if self.validarFormatoParlet(numero) == 'errorFormatoParlet':
                data['error'] = 'Error en el campo numero, formato no valido.'
                return JsonResponse(data, safe=False)
        else:
            if self.validarFormatoFC(numero) == 'errorFormatoFC':
                data['error'] = 'Error en el campo numero, formato no valido.'
                return JsonResponse(data, safe=False)

        try:
            if action == 'crearLimitado' and not Limitado.objects.filter(numero__exact=numero).exists():
                Limitado.objects.create(
                    numero=numero,
                    tipo=tipo,
                    precio=precio
                )
                if tipo == 1 or tipo == 2:
                    sms = f'Se ha limitado el numero {numero} correctamente.'
                    data['sms'] = sms
                else:
                    data['sms'] = f'Se ha limitado el parlet {numero} correctamente.'
            else:
                data['error'] = 'El numero entrado ya esta limitado.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Configuracion'
        context['limitados'] = self.get_queryset()
        context['tituloPestaña'] = 'ABC | Configuracion'
        return context

class topeView(LoginRequiredMixin, TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        action = request.POST['action']
        tope = request.POST['tope']
        data = {}
        try:
            query = Configuracion.objects.first()
            if action == 'topeBola':
                query.topeBola = request.POST['tope']
                query.save()
                sms = f'Nuevo tope para Bola establecido en {tope} correctamente.'
                data['sms'] = sms
            if action == 'topeCP':
                query.topeParlet = tope
                query.topeCentena = tope
                query.save()
                sms = f'Nuevo tope para Centena y parlet establecido en {tope} correctamente.'
                data['sms'] = sms
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

class jugadasEnviadasView(LoginRequiredMixin, TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def crearJugada(self, usuario, jugada, tipo, apostado, fecha):
        Jugada.objects.create(
            fk_usuario=usuario,
            numero=jugada,
            tipo=tipo,
            apostado=apostado,
            fecha=fecha
        )

    def post(self, request, *args, **kwargs):
        bruto = int(request.POST['bruto'])
        limpio = float(request.POST['limpio'])
        listaJugadas = json.loads(request.POST['listaJugadas'])
        fecha = datetime.datetime.today()
        data = {}
        try:
            for i in listaJugadas:
                if i['tipo'] == 'Fijo':
                    self.crearJugada(request.user, i['jugada'], 1, i['apostado'], fecha)
                elif i['tipo'] == 'Corrido':
                    self.crearJugada(request.user, i['jugada'], 2, i['apostado'], fecha)
                elif i['tipo'] == 'Centena':
                    self.crearJugada(request.user, i['jugada'], 4, i['apostado'], fecha)
                else:
                    Jugada.objects.create(
                        fk_usuario=request.user,
                        parlet=i['jugada'],
                        tipo=3,
                        apostado=i['apostado'],
                        fecha=fecha
                    )
            Contabilidad.objects.create(
                bruto=bruto,
                limpio=limpio,
                premio=0,
                fecha=fecha,
                fk_usuario=request.user
            )
            data['sms'] = 'Las jugadas se han guardado correctamente.'
        except Exception as e:
            print(e)
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

class getLimitadosView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        data, aux = {}, []
        try:
            query = Limitado.objects.all()
            for i in query:
                aux.append(i.toJSON())
            data['limitados'] = aux
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

class deleteLimitadoView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        data, aux = {}, []
        try:
            query = get_object_or_404(Limitado, numero=self.kwargs['pk'])
            if query.tipo == 1 or query.tipo == 2:
                sms = f'Se ha eliminado el numero {query.numero} como limitado.'
                data['sms'] = sms
            else:
                data['sms'] = f'Se ha eliminado el parlet {query.numero} como limitado.'
            query.delete()
            query = Limitado.objects.all()
            for i in query:
                aux.append(i.toJSON())
            data['limitados'] = aux
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

# PROCEDIMIENTO PARA LISTAR TIROS.
class listarTirosView(LoginRequiredMixin, ListView):
    template_name = 'charada/listar/tiros.html'
    model = Tiro

    def get_queryset(self):
        return Tiro.objects.last()

    def getJugadasBolasGanadoras(self):
        fecha = datetime.datetime.today()
        if horarioTarde():
            print('bolas gandoras tarde')
            query = Jugada.objects.filter(Q(tipo=1) | Q(tipo=2), fecha__day=fecha.date().day, fecha__hour__lt=16, esGanadora=True, fk_usuario=self.request.user).values(
                'numero', 'tipo', 'apostado', 'premio')
            if len(query) == 0:
                return False
            else:
                return query
        else:
            print('bolas gandoras noche')
            query = Jugada.objects.filter(Q(tipo=1) | Q(tipo=2), fecha__day=fecha.date().day, fecha__hour__gt=16, esGanadora=True, fk_usuario=self.request.user).values(
                'numero', 'tipo', 'apostado', 'premio')
            if len(query) == 0:
                return False
            else:
                return query



    def getJugadasParletGanadoras(self):
        fecha = datetime.datetime.today()
        if horarioTarde():
            query = Jugada.objects.filter(tipo=3, fecha__day=fecha.date().day, fecha__hour__lt=16, esGanadora=True,
                                          fk_usuario=self.request.user).values(
                'parlet', 'apostado', 'premio')
            if len(query) == 0:
                return False
            else:
                print(query)
                return query
        else:
            query = Jugada.objects.filter(tipo=3, fecha__day=fecha.date().day, fecha__hour__gt=16, esGanadora=True,
                                          fk_usuario=self.request.user).values(
                'parlet', 'apostado', 'premio')
            if len(query) == 0:
                return False
            else:
                return query

    def getJugadasCentenasGanadoras(self):
        fecha = datetime.datetime.today()
        if horarioTarde():
            query = Jugada.objects.filter(tipo=4, fecha__day=fecha.date().day, esGanadora=True, fecha__hour__lt=16, fk_usuario=self.request.user).values(
                'numero', 'apostado', 'premio')
            if len(query) == 0:
                return False
            else:
                return query
        else:
            query = Jugada.objects.filter(tipo=4, fecha__day=fecha.date().day, esGanadora=True, fecha__hour__gt=16, fk_usuario=self.request.user).values(
                'numero', 'apostado', 'premio')
            if len(query) == 0:
                return False
            else:
                return query

    def getContabilidadDelListero(self):
        data = {}
        fecha = datetime.datetime.today()
        try:
            if horarioTarde():
                query = Contabilidad.objects.get(fecha__day=fecha.date().day, fecha__hour__lt=16, fk_usuario=self.request.user)
                data['bruto'] = query.bruto
                data['limpio'] = query.limpio
                data['premio'] = query.premio
                return data
            else:
                query = Contabilidad.objects.get(fecha__day=fecha.date().day, fecha__hour__gt=16, fk_usuario=self.request.user)
                data['bruto'] = query.bruto
                data['limpio'] = query.limpio
                data['premio'] = query.premio
                return data
        except Exception as e:
            print(e)
            query = False
            return query

    def getContabilidadGeneral(self):
        data, aux = {}, []
        fecha = datetime.datetime.today()
        tiro = self.get_queryset()
        try:
            query = Contabilidad.objects.filter(fecha__day=fecha.date().day)
            if len(query) == 0:
                return False
            else:
                for i in query:
                    data = {'listero': i.fk_usuario, 'limpio': i.limpio, 'premio': i.premio}
                    aux.append(data)
                return aux
        except Exception as e:
            print(e)
            query = False
            return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tiro'] = self.get_queryset()
        context['contabilidad'] = self.getContabilidadDelListero()
        context['contabilidadGeneral'] = self.getContabilidadGeneral()
        context['bolas'] = self.getJugadasBolasGanadoras()
        context['parlets'] = self.getJugadasParletGanadoras()
        context['centenas'] = self.getJugadasCentenasGanadoras()
        context['titulo'] = 'Listado de Tiros'
        context['tituloPestaña'] = 'ABC | Projects'
        return context

# PROCEDIMIENTO PARA CREAR TIROS.
class crearTirosView(LoginRequiredMixin, CreateView):
    template_name = 'charada/crear/tiro.html'
    model = Tiro
    form_class = tiroForm
    success_url = reverse_lazy('charada:listarTiros')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        fecha = datetime.datetime.today()
        query = Tiro.objects.filter(fecha__day=fecha.date().day)
        if len(query) == 2:
            sms = 'No se pueden registrar mas tiros por el dia de hoy.'
            messages.error(self.request, sms)
        elif form.is_valid():
            messages.success(self.request, 'Tiro registrado correctamente.')
            form.save()
        else:
            messages.error(self.request, form.errors)
        return redirect('charada:listarTiros')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar nuevo tiro'
        context['tituloPestaña'] = 'SGPC | Cuadro'
        return context

# PROCEDIMIENTO PARA ELIMINAR TIRO.
class deleteTiroView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        data = {}
        try:
            query = get_object_or_404(Tiro, id=self.kwargs['pk'])
            messages.success(self.request, 'El tiro se ha eliminado correctamente.')
            data['url'] = 'http://127.0.0.1:8000/charada/listarTiros'
            query.delete()
        except Exception as e:
            messages.error(self.request, e)
            data['error'] = 'Ha ocurrido un error'
            data['url'] = 'http://127.0.0.1:8000/charada/listarTiros'
        return JsonResponse(data, safe=False)

class reporteGanaciaView(LoginRequiredMixin, TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validarFechaInicoVacia(self, fechaInicio):
        if fechaInicio == '':
            return 'fechaInicioVacia'

    def validarFechaFinVacia(self, fechaFin):
        if fechaFin == '':
            return 'fechaFinVacia'

    def validarFechas(self, fechaInicio, fechaFin):
        fechaInicial = datetime.datetime.strptime(fechaInicio, '%Y-%m-%d')
        fechaFinal = datetime.datetime.strptime(fechaFin, '%Y-%m-%d')

        if fechaFinal < fechaInicial:
            return 'error'

    def post(self, request, *args, **kwargs):
        fechaInicio = request.POST['fechaInicio']
        fechaFin = request.POST['fechaFin']
        data = {}
        limpio = 0
        premio = 0

        if self.validarFechaInicoVacia(fechaInicio) == 'fechaInicioVacia':
            data['error'] = 'La fecha inico es obligatoria.'
            return JsonResponse(data, safe=False)

        if self.validarFechaFinVacia(fechaFin) == 'fechaFinVacia':
            data['error'] = 'La fecha fin es obligatoria.'
            return JsonResponse(data, safe=False)

        if self.validarFechas(fechaInicio, fechaFin) == 'error':
            data['error'] = 'La fecha fin no puede ser menor que la fecha inicio.'
            return JsonResponse(data, safe=False)

        try:
            query = Contabilidad.objects.filter(fecha__range=(fechaInicio, fechaFin))
            for i in query:
                limpio += i.limpio
                premio += i.premio
            data['limpio'] = limpio
            data['premio'] = premio
            data['ganancia'] = limpio - premio
            data['sms'] = 'Las jugadas se han guardado correctamente.'
            return JsonResponse(data, safe=False)
        except Exception as e:
            print(e)
            data['error'] = str(e)
            return JsonResponse(data, safe=False)


