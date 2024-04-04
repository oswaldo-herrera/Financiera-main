from django.db.models.signals import post_save
from django.dispatch import receiver
from applications.dashboard.models import SimuladorPrueba
from applications.users.models import RegistroCreditosModel
from applications.calificaciones.models import IdentificadorDePago,IdentificadorDePagoRegistroMan
from datetime import timedelta


@receiver(post_save, sender=SimuladorPrueba)
def crear_identificadores_de_pago(sender, instance, created, **kwargs):
    if created:
        num_plazos = instance.nombre_prestamo.plazo

        # Obtener el número de plazos asociados con la instancia de SimuladorPrueba
        if (instance.nombre_prestamo.tipo_periodo.periodo_credito == 'Semanal'):
            periodo = 7
        elif (instance.nombre_prestamo.tipo_periodo.periodo_credito == 'Quincenal'):
            periodo = 15
        elif (instance.nombre_prestamo.tipo_periodo.periodo_credito == 'Mensual'):
            periodo = 30
        else:
            periodo = 30
        # determinar periodo de pago
        for num_plazo in range(1, num_plazos + 1):
            IdentificadorDePago.objects.create(
                simulador_relacionado=instance,
                periodo_a_pagar=num_plazo,
                monto_a_pagar=instance.nombre_prestamo.pago_mensual,
                monto_restante=instance.nombre_prestamo.pago_mensual,
                fecha_oportuna=instance.fecha_registro +
                (timedelta(days=periodo*num_plazo))

            )
            
            
@receiver(post_save, sender=RegistroCreditosModel)
def crear_identificadores_de_pago_manual(sender, instance, created, **kwargs):
    if created:
        num_plazos = instance.producto.plazo

        # Obtener el número de plazos asociados con la instancia de SimuladorPrueba
        if (instance.producto.tipo_periodo.periodo_credito == 'Semanal'):
            periodo = 7
        elif (instance.producto.tipo_periodo.periodo_credito == 'Quincenal'):
            periodo = 15
        elif (instance.producto.tipo_periodo.periodo_credito == 'Mensual'):
            periodo = 30
        else:
            periodo = 30
        # determinar periodo de pago
        for num_plazo in range(1, num_plazos + 1):
            IdentificadorDePagoRegistroMan.objects.create(
                simulador_relacionado=instance,
                periodo_a_pagar=num_plazo,
                monto_a_pagar=instance.producto.pago_mensual,
                monto_restante=instance.producto.pago_mensual,
                fecha_oportuna=instance.fecha_credito +
                (timedelta(days=periodo*num_plazo))

            )
