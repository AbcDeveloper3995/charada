import datetime
from crum import get_current_user
from django.db import models
from django.db.models.signals import post_save
from django.forms import model_to_dict

from apps.usuario.models import Usuario

CHOICE_TIPO_JUGADA = (
    (1, 'Fijo'),
    (2, 'Corrido'),
    (3, 'Parlet'),
    (4, 'Centena')
)

CHOICE_HORARIO = (
    ('Tarde', 'Tarde'),
    ('Noche', 'Noche')
)

CHOICE_MODOS = (
    (1, 'Lista'),
    (2, 'Bote')
)

class Limitado(models.Model):
    numero = models.CharField(verbose_name='Numero limitado', max_length=7, blank=False, null=False)
    tipo = models.PositiveIntegerField(verbose_name='Para que tipo de jugada', blank=False, null=False, choices=CHOICE_TIPO_JUGADA)
    precio = models.PositiveIntegerField(verbose_name='Precio para el premio', blank=False, null=False)

    class Meta:
        db_table = 'Limitado'
        verbose_name = 'Limitado'
        verbose_name_plural = 'Limitados'
        ordering = ['numero']

    def __str__(self):
        return 'Limitado: {0}, para {1}, precio a pagar {2}'.format(self.numero, self.getClaveTipo(), self.precio)

    def toJSON(self):
        item = model_to_dict(self)
        item['numero'] = self.numero
        item['tipo'] = self.tipo
        return item

    def getClaveTipo(self):
        if self.tipo == 1:
            return 'Fijo'
        if self.tipo == 2:
            return 'Corrido'
        if self.tipo == 3:
            return 'Parlet'

class Tiro(models.Model):
    primerNumero = models.PositiveIntegerField(verbose_name='Primer numero', blank=False, null=False)
    fijoCorrido = models.PositiveIntegerField(verbose_name='Primer numero fijo corrido', blank=False, null=False)
    primerCorrido = models.PositiveIntegerField(verbose_name='Primer numero corrido', blank=False, null=False)
    segundoCorrido = models.PositiveIntegerField(verbose_name='Segundo numero corrido', blank=False, null=False)
    fecha = models.DateField(verbose_name='Fecha del tiro', auto_now=True)
    horario = models.CharField(verbose_name='Horario del tiro', max_length=10, blank=False, null=False, choices=CHOICE_HORARIO)

    class Meta:
        db_table = 'Tiro'
        verbose_name = 'Tiro'
        verbose_name_plural = 'Tiros'

    def __str__(self):
        return 'Tiro de la {0}, del dia {1}'.format(self.horario, self.fecha)

    def getListaConLosTresNumerosCorridos(self):
        aux = []
        aux.append(self.fijoCorrido)
        aux.append(self.primerCorrido)
        aux.append(self.segundoCorrido)
        return aux

    def getCentena(self):
        centena = str(self.primerNumero)+str(self.fijoCorrido)
        return centena



class Jugada(models.Model):
    fk_usuario = models.ForeignKey(Usuario, verbose_name='Persona que entra la jugada', blank=False, null=False, on_delete=models.CASCADE)
    fk_tiro = models.ForeignKey(Tiro, verbose_name='Tiro', blank=True, null=True, on_delete=models.SET_NULL)
    numero = models.PositiveIntegerField(verbose_name='numero', blank=True, null=True)
    tipo = models.PositiveIntegerField(verbose_name='Tipo de jugada', blank=False, null=False, choices=CHOICE_TIPO_JUGADA)
    apostado = models.PositiveIntegerField(verbose_name='Apostado a la jugada', blank=False, null=False)
    premio = models.PositiveIntegerField(verbose_name='Premio', default=0, blank=True, null=True)
    fecha = models.DateTimeField(verbose_name='Fecha de entrada de las jugadas')
    parlet = models.CharField(max_length=5, blank=True, null=True)
    esGanadora = models.BooleanField(verbose_name='Jugada ganadora', default=False)

    class Meta:
        db_table = 'Jugada'
        verbose_name = 'Jugada'
        verbose_name_plural = 'Jugadas'

    def __str__(self):
        return '{0} pesos al {1} {2} dia {3}'.format(self.apostado, self.numero if self.tipo != 3 else self.parlet, self.getClaveTipo(), self.fecha)

    def getClaveTipo(self):
        if self.tipo == 1:
            return 'Fijo'
        if self.tipo == 2:
            return 'Corrido'
        if self.tipo == 3:
            return 'Parlet'
        if self.tipo == 4:
            return 'Centena'

class Configuracion(models.Model):
    modo = models.PositiveIntegerField(verbose_name='Modo', blank=True, null=True, choices=CHOICE_MODOS)
    topeBola = models.PositiveIntegerField(verbose_name='Tope para Bola', blank=True, null=True)
    topeParlet = models.PositiveIntegerField(verbose_name='Tope para parlet', blank=True, null=False)
    topeCentena = models.PositiveIntegerField(verbose_name='Tope para centena', blank=True, null=True)

    class Meta:
        db_table = 'Configuracion'
        verbose_name = 'Configuracion'
        verbose_name_plural = 'Configuraciones'

    def __str__(self):
        return 'Configuracion: {0} {1} {2} {3}'.format(self.modo, self.topeBola, self.topeParlet, self.topeCentena)


class Logs(models.Model):
    fk_usuario = models.ForeignKey(Usuario, verbose_name='Persona que entra la jugada', related_name='jugada_usuario', blank=False, null=False, on_delete=models.CASCADE)
    descripcion = models.CharField(verbose_name='Descripcion', max_length=255, blank=True, null=True)
    fecha = models.DateField(verbose_name='Fecha de la jugada', auto_now=True)

    class Meta:
        db_table = 'Logs'
        verbose_name = 'Logs'
        verbose_name_plural = 'Logs'

    def __str__(self):
        return 'El usuario {0} realizo la siguiente accio: {1}, el dia {2}'.format(self.fk_usuario.username, self.descripcion, self.fecha)


class Contabilidad(models.Model):
    fk_tiro = models.ForeignKey(Tiro, verbose_name='Tiro', blank=True, null=True, on_delete=models.SET_NULL)
    fk_usuario = models.ForeignKey(Usuario, verbose_name='Usuario', blank=True, null=True, on_delete=models.CASCADE)
    bruto = models.PositiveIntegerField(verbose_name='Bruto', blank=False, null=False)
    limpio = models.PositiveIntegerField(verbose_name='Limpio', blank=False, null=False)
    premio = models.PositiveIntegerField(verbose_name='Premio', blank=False, null=False)
    fecha = models.DateTimeField(verbose_name='Fecha de entrada de las jugadas')

    class Meta:
        db_table = 'Contabilidad'
        verbose_name = 'Contabilidad'
        verbose_name_plural = 'Contabilidad'

    def __str__(self):
        return 'Contabilidad del dia {0} del listero {1}, Bruto:{2},  Limpio:{3}, Premio:{4} -- {5}'.format(self.fecha.date(), self.fk_usuario.username, self.bruto, self.limpio, self.premio, self.getHorario())

    def getSoloFecha(self):
        return self.fecha.date()

    def getHorario(self):
        if self.fecha.hour > 14:
            return "Tarde"
        else:
            return 'Noche'


def calcularPremio(sender, instance, **kwargs):
    listaLimitados, jugadasFijas, jugadasCorridas, jugadasParlet, jugadasCentenas = [], [], [], [], []
    fecha = datetime.datetime.today()
    tiro = Tiro.objects.last()

    # FORMAR UNA LISTA CON LOS NUMEROS LIMITADOS
    limitados = Limitado.objects.all().values('numero')
    for i in limitados:
        listaLimitados.append(i['numero'])

    if tiro.horario == 'Tarde':
        print('jugadas de la tarde')
        #SEPARAR LAS JUGADAS POR TIPO
        try:
            jugadasTarde = Jugada.objects.filter(fecha__day=fecha.date().day, fecha__hour__lt=16)
            for i in jugadasTarde:
                i.fk_tiro = tiro
                i.save()
                if i.tipo == 1:
                    jugadasFijas.append(i)
                if i.tipo == 2:
                    jugadasCorridas.append(i)
                if i.tipo == 3:
                    jugadasParlet.append(i)
                if i.tipo == 4:
                    jugadasCentenas.append(i)
        except Exception as e:
            print(e)
            print('No se ha realizado el tiro de la tarde')

        for i in jugadasFijas:
            if i.numero == tiro.fijoCorrido and str(i.numero) in listaLimitados:
                objLimitado = Limitado.objects.get(numero=i.numero)
                if objLimitado.tipo == 1:
                    i.premio = i.apostado * objLimitado.precio
                    i.esGanadora = True
                    i.save()
                    print('fijo esta y es limitado')

            if i.numero == tiro.fijoCorrido and str(i.numero) not in listaLimitados:
                i.premio = i.apostado * 75
                i.esGanadora = True
                i.save()
                print('fijo esta y no es limitado')

        for i in jugadasCorridas:
            if i.numero in tiro.getListaConLosTresNumerosCorridos() and str(i.numero) in listaLimitados:
                objLimitado = Limitado.objects.get(numero=i.numero)
                if objLimitado.tipo == 2:
                    i.premio = i.apostado * objLimitado.precio
                    i.esGanadora = True
                    i.save()
                else:
                    i.premio = i.apostado * 25
                    i.esGanadora = True
                    i.save()
            if i.numero in tiro.getListaConLosTresNumerosCorridos() and str(i.numero) not in listaLimitados:
                i.premio = i.apostado * 25
                i.esGanadora = True
                i.save()

        for i in jugadasCentenas:
            if i.numero == int(tiro.getCentena()):
                i.premio = i.apostado * 400
                i.esGanadora = True
                i.save()
                print('centena esta')
            print('centena no esta')

        for i in jugadasParlet:
            primerNumero = int(i.parlet[0:2])
            segundoNumero = int(i.parlet[3:5])
            print(primerNumero, segundoNumero)
            if primerNumero in tiro.getListaConLosTresNumerosCorridos() and segundoNumero in tiro.getListaConLosTresNumerosCorridos() and i.parlet in listaLimitados:
                objLimitado = Limitado.objects.get(numero=i.parlet)
                i.premio = i.apostado * objLimitado.precio
                i.esGanadora = True
                i.save()
            elif primerNumero in tiro.getListaConLosTresNumerosCorridos() and segundoNumero in tiro.getListaConLosTresNumerosCorridos():
                i.premio = i.apostado * 1100
                i.esGanadora = True
                i.save()

        try:
            usuario = Usuario.objects.all()
            for i in usuario:
                premio = 0
                obj = Contabilidad.objects.filter(fk_usuario=i, fecha__day=fecha.date().day, fecha__hour__lt=16)
                if obj.exists():
                    obj.update(fk_tiro=tiro)
                    lista = Jugada.objects.filter(fk_usuario=i, esGanadora=True, fecha__day=fecha.date().day,
                                                  fecha__hour__lt=16)
                    for j in lista:
                        premio += j.premio
                    obj.update(premio=premio)
                else:
                    print('no exite cont para', i)
        except Exception as e:
            print(e)
            print('No se ha realizado el tiro de la tarde')
    else:
        print('jugadas de la noche')
        # SEPARAR LAS JUGADAS POR TIPO
        try:
            jugadasNoche = Jugada.objects.filter(fecha__day=fecha.date().day, fecha__hour__gt=16)
            for i in jugadasNoche:
                i.fk_tiro = tiro
                i.save()
                if i.tipo == 1:
                    jugadasFijas.append(i)
                if i.tipo == 2:
                    jugadasCorridas.append(i)
                if i.tipo == 3:
                    jugadasParlet.append(i)
                if i.tipo == 4:
                    jugadasCentenas.append(i)
        except Exception as e:
            print(e)
            print('No se ha realizado el tiro de la tarde')

        for i in jugadasFijas:
            if i.numero == tiro.fijoCorrido and str(i.numero) in listaLimitados:
                objLimitado = Limitado.objects.get(numero=i.numero)
                if objLimitado.tipo == 1:
                    i.premio = i.apostado * objLimitado.precio
                    i.esGanadora = True
                    i.save()
                    print('fijo esta y es limitado')

            if i.numero == tiro.fijoCorrido and str(i.numero) not in listaLimitados:
                i.premio = i.apostado * 75
                i.esGanadora = True
                i.save()
                print('fijo esta y no es limitado')

        for i in jugadasCorridas:
            if i.numero in tiro.getListaConLosTresNumerosCorridos() and str(i.numero) in listaLimitados:
                objLimitado = Limitado.objects.get(numero=i.numero)
                if objLimitado.tipo == 2:
                    i.premio = i.apostado * objLimitado.precio
                    i.esGanadora = True
                    i.save()
                else:
                    i.premio = i.apostado * 25
                    i.esGanadora = True
                    i.save()
            if i.numero in tiro.getListaConLosTresNumerosCorridos() and str(i.numero) not in listaLimitados:
                i.premio = i.apostado * 25
                i.esGanadora = True
                i.save()

        for i in jugadasCentenas:
            if i.numero == int(tiro.getCentena()):
                i.premio = i.apostado * i.apostado * 400
                i.esGanadora = True
                i.save()
                print('centena esta')
            print('centena no esta')

        for i in jugadasParlet:
            primerNumero = int(i.parlet[0:2])
            segundoNumero = int(i.parlet[3:5])
            print(primerNumero, segundoNumero)
            if primerNumero in tiro.getListaConLosTresNumerosCorridos() and segundoNumero in tiro.getListaConLosTresNumerosCorridos() and i.parlet in listaLimitados:
                objLimitado = Limitado.objects.get(numero=i.parlet)
                i.premio = i.apostado * objLimitado.precio
                i.esGanadora = True
                i.save()
            elif primerNumero in tiro.getListaConLosTresNumerosCorridos() and segundoNumero in tiro.getListaConLosTresNumerosCorridos():
                i.premio = i.apostado * 1100
                i.esGanadora = True
                i.save()

        try:
            usuario = Usuario.objects.all()
            for i in usuario:
                premio = 0
                obj = Contabilidad.objects.filter(fk_usuario=i, fecha__day=fecha.date().day, fecha__hour__gt=16)
                if obj.exists():
                    obj.update(fk_tiro=tiro)
                    lista = Jugada.objects.filter(fk_usuario=i, esGanadora=True, fecha__day=fecha.date().day,
                                                  fecha__hour__gt=16)
                    for j in lista:
                        premio += j.premio
                    obj.update(premio=premio)
                else:
                    print('no exite cont para', i)
        except Exception as e:
            print(e)
            print('No se ha realizado el tiro de la tarde')

post_save.connect(calcularPremio, sender=Tiro)