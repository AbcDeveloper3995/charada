from django.contrib import admin
from apps.charada.models import *



class JugadaAdmin(admin.ModelAdmin):
    search_fields = ('numero', 'parlet', 'apostado')

admin.site.register(Limitado)
admin.site.register(Tiro)
admin.site.register(Jugada, JugadaAdmin)
admin.site.register(Configuracion)
admin.site.register(Logs)
admin.site.register(Contabilidad)

