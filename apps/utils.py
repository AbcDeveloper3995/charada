import datetime

from django.shortcuts import render
#ESTABLECER HORARIOS
def definirAMoPM():
    hora = datetime.datetime.now().strftime('%I:%M:%S %p')
    if horarioTarde():
        return 'AM'
    else:
        return 'PM'


def horarioTarde():
    hoy = datetime.datetime.today()
    anoActual = datetime.datetime.today().year
    mesActual = datetime.datetime.today().month
    diaActual = datetime.datetime.today().day
    aperturaTexto = f'{anoActual}-{mesActual}-{diaActual} 07:00:00 AM'
    cierreTexto = f'{anoActual}-{mesActual}-{diaActual} 02:30:00 PM'
    apertura = datetime.datetime.strptime(aperturaTexto, '%Y-%m-%d %I:%M:%S %p')
    cierre = datetime.datetime.strptime(cierreTexto, '%Y-%m-%d %I:%M:%S %p')
    if hoy > apertura and hoy < cierre:
        return True
    else:
        return False


def horarioNoche():
    hoy = datetime.datetime.today()
    anoActual = datetime.datetime.today().year
    mesActual = datetime.datetime.today().month
    diaActual = datetime.datetime.today().day
    aperturaTexto = f'{anoActual}-{mesActual}-{diaActual} 02:00:00 PM'
    cierreTexto = f'{anoActual}-{mesActual}-{diaActual} 9:30:00 PM'
    apertura = datetime.datetime.strptime(aperturaTexto, '%Y-%m-%d %I:%M:%S %p')
    cierre = datetime.datetime.strptime(cierreTexto, '%Y-%m-%d %I:%M:%S %p')
    print(hoy)
    if hoy > apertura and hoy < cierre:
        return True
    else:
        return False

#FUNCIONES PARA CAPTURAR LOS ERRORES 400, 403, 404, 500
def badRequest403(request, exception):
    return render(request, '400.html')

def permissionDenied403(request, exception):
    return render(request, '403.html')

def pageNotFound404(request, exception):
    return render(request, '404.html')

def internalError500(request, exception):
    return render(request, '500.html')
