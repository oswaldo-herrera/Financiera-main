from django.contrib import admin
from .models import RegistroCreditos,EstatusCredito,RegistroPagosModel,IdentificadorDePago,IdentificadorDePagoRegistroMan,RegistroPagosModelManual

# Register your models here.

class IdentificadorDePagoAdmin(admin.ModelAdmin):
    list_display = ('simulador_relacionado', 'periodo_a_pagar', 'fecha_oportuna',
                    'monto_a_pagar', 'monto_restante', 'estatus',)


class RegistroPagosModelAdmin(admin.ModelAdmin):
    list_display = ('simulador', 'monto_pagado', 'fecha_pago',
                    'periodo_a_pagar', 'identificador',)



admin.site.register(RegistroCreditos)
admin.site.register(EstatusCredito)
admin.site.register(RegistroPagosModel, RegistroPagosModelAdmin)
admin.site.register(IdentificadorDePago, IdentificadorDePagoAdmin)
admin.site.register(IdentificadorDePagoRegistroMan)
admin.site.register(RegistroPagosModelManual)

