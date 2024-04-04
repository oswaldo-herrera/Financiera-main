from typing import Any
import sympy as yaab
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from decimal import Decimal
from django.views.generic import TemplateView,ListView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from applications.users.models import User,EstadoCivilValues,RegistroCreditosModel
from applications.dashboard.models import SimuladorPrueba
from .models import RegistroCreditos,EstatusCredito,RegistroPagosModel,IdentificadorDePago,IdentificadorDePagoRegistroMan,RegistroPagosModelManual
from .forms import RegistroPagosForm,RegistroPagosFormManual
from datetime import timedelta,datetime
from django.utils import timezone
from django.urls import reverse_lazy,reverse
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View
#from dateutil.relativedelta import relativedelta
from django.db.models import Sum






# Create your views here.



class ControlCalificaciones(ListView):
    template_name = 'calificaciones/control-calificaciones.html'
    context_object_name = 'usuarios'
    
    def get_queryset(self):
        
        usuarios_filtro = EstadoCivilValues.objects.all()      
        
        return usuarios_filtro

    def get_context_data(self, **kwargs) :
        context = super(ControlCalificaciones,self).get_context_data(**kwargs)
        usuarios = EstadoCivilValues.objects.filter(valor_numerico_edad__isnull=False,
        valor_numerico_estado_civil__isnull=False,
        valor_numerico_empleo__isnull=False)
        
        suma_total = 0
        
        
        for usuario in usuarios:
            suma_total += (usuario.valor_numerico_edad or 0) + (usuario.valor_numerico_estado_civil or 0) + (usuario.valor_numerico_empleo or 0)
            # suma_total += usuario.valor_numerico_edad + usuario.valor_numerico_estado_civil + usuario.valor_numerico_empleo
        
        context['cliente'] =usuarios
        context["suma_total"] = suma_total
        return context
    
    
class ViewRegistroCreditos(ListView):
    template_name = "calificaciones/registro-creditos.html"
    context_object_name = 'registros'
        
    def get_queryset(self):
        
        #registro_usuarios = User.objects.filter(solicitud=True)
        registro_usuarios = RegistroCreditos.objects.filter(cliente__solicitud=True)
        
        return registro_usuarios
    
class ViewCreditosStatusEstatico(ListView):
    template_name = 'calificaciones/creditos-estatus-estatico.html'
    context_object_name ='estatus'
    
    def get_queryset(self):
        
        usuarios_con_solicitud_true = User.objects.filter(solicitud=True)
        estatus_usuarios = SimuladorPrueba.objects.filter(usuario_user__in=usuarios_con_solicitud_true)
        
        simuladores_data = []
        
        for simulador in estatus_usuarios:
            usuario = simulador.usuario_user
        
            numero_contrato = simulador.identificador_unico
            nombre_usuario = usuario.first_name + usuario.last_name
            fecha_desembolso = usuario.fecha_solicitud
            monto_total_calculado = simulador.nombre_prestamo.monto * Decimal(simulador.nombre_prestamo.interes_moratorio)
            desembolso = simulador.nombre_prestamo.monto - (simulador.nombre_prestamo.monto * 0.05)
            pago_men = simulador.nombre_prestamo.pago_mensual
            tiempo = simulador.nombre_prestamo.plazo
            monto_pagado_hasta_hoy = simulador.nombre_prestamo.pago_mensual * 4
            saldo_pendiente = monto_total_calculado - monto_pagado_hasta_hoy
            monto_morosidad_calculo = (pago_men * Decimal(1.2)) * 3
            saldo_mas_morosidad_return = saldo_pendiente + monto_morosidad_calculo

            fecha_proxima = simulador.usuario_user.fecha_proximo_viernes.replace(tzinfo=timezone.utc) if simulador.usuario_user.fecha_proximo_viernes else None
            registros_previos = SimuladorPrueba.objects.filter(usuario_user=usuario).exclude(pk=simulador.pk)

            if registros_previos.exists():
                tipo = 'Renovado'
            else:
                tipo = 'Nuevo'

            if fecha_proxima:
                estatus = 'Atraso' if timezone.now() > fecha_proxima else 'Al corriente'
            else:
                estatus = 'Fecha próxima no disponible'

            simulador_data = {
                'numero_contrato': numero_contrato,
                'nombre_usuario': nombre_usuario,
                'fecha_desembolso': fecha_desembolso,
                'monto_total_calculado': monto_total_calculado,
                'desembolso': desembolso,
                'pago_mensual': pago_men,
                'tiempo': tiempo,
                'monto_pagado_hasta_hoy': monto_pagado_hasta_hoy,
                'saldo_pendiente': saldo_pendiente,
                'monto_morosidad': monto_morosidad_calculo,
                'saldo_mas_morosidad': saldo_mas_morosidad_return,
                'tipo': tipo,
                'estatus': estatus,
                
            }

            simuladores_data.append(simulador_data)
        
        return simuladores_data
    
# def calcular_corrida_financiera(self, pago_mensual, plazo, fecha_solicitud, monto_pagado = None, frecuencia_pago='semanal'):
    #     detalles_pago = []        
    #     fecha_actual = fecha_solicitud
        
        
        
    #     if fecha_solicitud is None:
    #         fecha_solicitud = datetime.now().date()  # Asigna la fecha actual si no hay fecha de solicitud
            
    #     for numero_pago in range(1, plazo + 1):
            
    #         if frecuencia_pago == 'semanal':
    #             fecha_pago_estimada = fecha_solicitud + timedelta(weeks=numero_pago)
    #         elif frecuencia_pago == 'mensual':
    #             fecha_pago_estimada = fecha_solicitud + timedelta(days=30 * numero_pago) 
            
            
    #         diferencia = fecha_pago_estimada - fecha_solicitud
            
    #         detalle_pago = {
    #             'numero_pago': numero_pago,
    #             'fecha_pago': fecha_solicitud,
    #             'pago_mensual': pago_mensual
    #         }
    #         # Si es el primer pago y se proporciona el monto pagado, establecerlo
    #         if diferencia.days >= 0:
    #             detalle_pago = {
    #                 'numero_pago': numero_pago,
    #                 'fecha_pago': fecha_pago_estimada,
    #                 'pago_mensual': pago_mensual,
    #                 'diferencia_pago': diferencia.days,
    #                 'monto_pagado': 0,  # Inicialmente, no se ha realizado ningún pago
    #                 'estado_pago': pago_mensual  # Inicialmente, el estado del pago es el monto completo
    #             }
                
    #             detalles_pago.append(detalle_pago)


    #     return detalles_pago
        
    
    
    ### el estable bien ######
    # def calcular_corrida_financiera(self, pago_mensual, plazo, fecha_solicitud, monto_pagado = None, frecuencia_pago='semanal'):
    #     detalles_pago = []        
    #     fecha_actual = fecha_solicitud
        
    #     if fecha_actual is None:
    #         fecha_actual = timezone.now().date()  # Asigna la fecha actual si no hay fecha de solicitud
    #     for numero_pago in range(1, plazo + 1):
    #         detalle_pago = {
    #             'numero_pago': numero_pago,
    #             'fecha_pago': fecha_actual,
    #             'pago_mensual': pago_mensual
    #         }
    #         # Si es el primer pago y se proporciona el monto pagado, establecerlo
    #         if numero_pago == 1 and monto_pagado is not None:
    #             diferencia =  pago_mensual - monto_pagado
    #             detalle_pago['monto_pagado'] = monto_pagado
    #             detalle_pago['diferencia_pago'] = diferencia
    #             if diferencia == 0 or monto_pagado == 0:
    #                 detalle_pago['estado_pago'] = 0
    #             else:
    #                 detalle_pago['estado_pago'] = diferencia
    #         detalles_pago.append(detalle_pago)
    #         # Actualizar la fecha para el próximo pago según la frecuencia de pago
    #         if frecuencia_pago == 'semanal':
    #             fecha_actual += timedelta(days=7)
    #         elif frecuencia_pago == 'mensual':
    #             fecha_actual += timedelta(days=30)  # Suponiendo meses de 30 días para simplificar

    #     return detalles_pago
    
    # def calcular_corrida_financiera(self, pago_mensual, plazo, fecha_solicitud, monto_pagado = None, frecuencia_pago='semanal'):
    #     detalles_pago = []
        
    #     fecha_actual = fecha_solicitud
    #     if fecha_actual is None:
    #         fecha_actual = timezone.now().date()  # Asigna la fecha actual si no hay fecha de solicitud
    #     for numero_pago in range(1, plazo + 1):
    #         detalle_pago = {
    #             'numero_pago': numero_pago,
    #             'fecha_pago': fecha_actual,
    #             'pago_mensual': pago_mensual
    #         }
    #         # Si es el primer pago y se proporciona el monto pagado, establecerlo
    #         if numero_pago == 1 and monto_pagado is not None:
    #             diferencia =  pago_mensual - monto_pagado
    #             detalle_pago['monto_pagado'] = monto_pagado
    #             detalle_pago['diferencia_pago'] = diferencia
    #             if diferencia == 0 or monto_pagado == 0:
    #                 detalle_pago['estado_pago'] = 0
    #             else:
    #                 detalle_pago['estado_pago'] = diferencia
    #         detalles_pago.append(detalle_pago)
    #         # Actualizar la fecha para el próximo pago según la frecuencia de pago
    #         if frecuencia_pago == 'semanal':
    #             fecha_actual += timedelta(days=7)
    #         elif frecuencia_pago == 'mensual':
    #             fecha_actual += timedelta(days=30)  # Suponiendo meses de 30 días para simplificar

    #     return detalles_pago


    
class ViewCreditosStatus(ListView):
    template_name = "calificaciones/creditos-estatus.html"
    context_object_name = 'estatus'

       
    def get_queryset(self):
        estatus_usuarios = SimuladorPrueba.objects.all()
        # usuarios_con_solicitud_true = User.objects.filter(solicitud=True)
        # estatus_usuarios = SimuladorPrueba.objects.filter(usuario_user__in=usuarios_con_solicitud_true)
        creditos_registro = RegistroCreditosModel.objects.all()
        
        simuladores_data = []

        # monto_pagado_hasta_hoy = 0

        for simulador in estatus_usuarios:
            usuario = simulador.usuario_user
            #identificador_prestamo = IdentificadorDePago.objects.get(simulador_relacionado=simulador)
            identificador_prestamo = IdentificadorDePago.objects.filter(simulador_relacionado=simulador).order_by('id')

            # ultimo_pago_registrado = RegistroPagosModel.objects.filter(simulador=simulador).order_by('-numero_pago').first()
            # numero_pago = ultimo_pago_registrado.numero_pago if ultimo_pago_registrado else 0

            # monto_pagado = RegistroPagosModel.objects.filter(
            #     simulador=simulador).aggregate(Sum('monto_pagado'))['monto_pagado__sum']

            # monto_pagado = monto_pagado or 0

            
            numero_contrato = simulador.identificador_unico
            nombre_usuario = usuario.first_name + usuario.last_name
            fecha_desembolso = usuario.fecha_solicitud
            monto_total_calculado = simulador.nombre_prestamo.monto * \
                Decimal(simulador.nombre_prestamo.interes_moratorio)
            desembolso = simulador.nombre_prestamo.monto - \
                (simulador.nombre_prestamo.monto * 0.05)
            pago_men = simulador.nombre_prestamo.pago_mensual
            tiempo = simulador.nombre_prestamo.plazo
            monto_pagado_hasta_hoy = simulador.nombre_prestamo.pago_mensual * 4
            #monto_pagado_hasta_hoy = identificador_prestamo.monto_restante
            saldo_pendiente = monto_total_calculado - monto_pagado_hasta_hoy
            monto_morosidad_calculo = (pago_men * Decimal(1.2)) * 3
            saldo_mas_morosidad_return = saldo_pendiente + monto_morosidad_calculo

            fecha_proxima = simulador.usuario_user.fecha_proximo_viernes.replace(
                tzinfo=timezone.utc) if simulador.usuario_user.fecha_proximo_viernes else None
            registros_previos = SimuladorPrueba.objects.filter(
                usuario_user=usuario).exclude(pk=simulador.pk)

            if registros_previos.exists():
                tipo = 'Renovado'
            else:
                tipo = 'Nuevo'

            if fecha_proxima:
                estatus = 'Atraso' if timezone.now() > fecha_proxima else 'Al corriente'
            else:
                estatus = 'Fecha próxima no disponible'

            simulador_data = {
                'numero_contrato': numero_contrato,
                'nombre_usuario': nombre_usuario,
                'fecha_desembolso': fecha_desembolso,
                'monto_total_calculado': monto_total_calculado,
                'desembolso': desembolso,
                'pago_mensual': pago_men,
                'tiempo': tiempo,
                'monto_pagado_hasta_hoy': monto_pagado_hasta_hoy,
                'saldo_pendiente': saldo_pendiente,
                'monto_morosidad': monto_morosidad_calculo,
                'saldo_mas_morosidad': saldo_mas_morosidad_return,
                'tipo': tipo,
                'estatus': estatus,
                'corrida': identificador_prestamo,
            }

            simuladores_data.append(simulador_data)
            
        for credito in creditos_registro:
            usuario_manual = credito.usuarios
            
            identificador_prestamo = IdentificadorDePagoRegistroMan.objects.filter(simulador_relacionado=credito).order_by('id')
            registro_pagos_manual = RegistroPagosModelManual.objects.filter(simulador=credito)
            # for  pago_mensual in registro_pagos_manual:
            #     monto_pagado_hasta_hoy = pago_mensual.monto_pagado
                
                        
            numero_contrato = credito.identificador_unico
            nombre_usuario = credito.usuarios.username
            fecha_desembolso = credito.fecha_credito
            monto_total_calculado = credito.producto.monto * \
                Decimal(credito.producto.interes_moratorio)
            desembolso = credito.producto.monto - \
                (credito.producto.monto * 0.05)
            pago_men = credito.producto.pago_mensual
            tiempo = credito.producto.plazo
            #monto_pagado_hasta_hoy = credito.producto.pago_mensual * 4
            monto_pagado_hasta_hoy = registro_pagos_manual.aggregate(total_pagado=Sum('monto_pagado'))['total_pagado']            
            # saldo_pendiente = monto_total_calculado - monto_pagado_hasta_hoy
            saldo_pendiente = 1234
            monto_morosidad_calculo = (pago_men * Decimal(1.2)) * 3
            saldo_mas_morosidad_return = saldo_pendiente + monto_morosidad_calculo
            
            fecha_proxima = credito.usuarios.fecha_proximo_viernes.replace(
                tzinfo=timezone.utc) if credito.usuarios.fecha_proximo_viernes else None
            registros_previos = RegistroCreditosModel.objects.filter(
                usuarios=usuario_manual).exclude(pk=credito.pk)

            if registros_previos.exists():
                tipo = 'Renovado'
            else:
                tipo = 'Nuevo'

            if fecha_proxima:
                estatus = 'Atraso' if timezone.now() > fecha_proxima else 'Al corriente'
            else:
                estatus = 'Fecha próxima no disponible'
                
            registro_data = {
                'numero_contrato': numero_contrato,
                'nombre_usuario': nombre_usuario,
                'fecha_desembolso': fecha_desembolso,
                'monto_total_calculado':monto_total_calculado,  
                'desembolso': desembolso,  
                'pago_mensual': pago_men,  
                'tiempo': tiempo,  
                'monto_pagado_hasta_hoy': monto_pagado_hasta_hoy,  
                'saldo_pendiente': saldo_pendiente,  
                'monto_morosidad': monto_morosidad_calculo,  
                'saldo_mas_morosidad': saldo_mas_morosidad_return,  
                'tipo': tipo,  
                'estatus': estatus,  
                'corrida': identificador_prestamo,  
            }
            simuladores_data.append(registro_data)
            
            

        return simuladores_data 

    def post(self, request, *args, **kwargs):
        form = RegistroPagosForm(request.POST, request.FILES)
        if form.is_valid():
            # Obtener el simulador seleccionado del formulario
            simulador_id = request.POST.get('simulador')
            simulador = SimuladorPrueba.objects.get(id=simulador_id)

            # Guardar el formulario
            registro_pago = form.save(commit=False)

            # Asignar el simulador al registro de pago
            registro_pago.simulador = simulador
            registro_pago.save()

            # Obtener el monto del pago registrado
            monto_pagado = registro_pago.monto_pagado
            # numero_pago = registro_pago.numero_pago

            # Obtener la corrida financiera del simulador
            corrida_financiera = self.calcular_corrida_financiera(
                simulador.nombre_prestamo.pago_mensual,
                simulador.nombre_prestamo.plazo,
                simulador.usuario_user.fecha_solicitud
            )

            for pago in corrida_financiera:
                if pago['numero_pago'] == monto_pagado:
                    # Actualizar el monto pagado del pago correspondiente
                    pago['monto_pagado'] = registro_pago.monto_pagado
                    pago['estado_pago'] = pago['pago_mensual'] - \
                        registro_pago.monto_pagado
                    break

            # Guardar la corrida financiera actualizada en el simulador

            simulador.save()

# ****************************************************************************************************************************************
 # 
            # Obtener el objeto SimuladorPrueba seleccionado del formulario
            simulador = form.cleaned_data['simulador']

            # Obtener el monto pagado del formulario
            monto_pagado = form.cleaned_data['monto_pagado']

            periodos = IdentificadorDePago.objects.filter(
                simulador_relacionado=simulador, estatus=False)
            # array con los periodos sin pagar
            numero_periodos = len(periodos)

            if (numero_periodos > 0):

                periodo_pendiente = IdentificadorDePago.objects.filter(
                    simulador_relacionado=simulador, estatus=False).order_by('periodo_a_pagar').first()
                # periodo mas reciente sin pagar

                periodo_pendiente.monto_restante = periodo_pendiente.monto_restante - monto_pagado

                if (periodo_pendiente.monto_restante <= 0):
                    periodo_pendiente.estatus = True
                    numero_periodos = numero_periodos-1
                    # cambia estado de periodo a pagado y le resto 1 al numero de periodos pendientes

                periodo_pendiente.save()
                # guarde la instancia

                while (periodo_pendiente.monto_restante < 0 and numero_periodos > 0):
                    monto_pagado = periodo_pendiente.monto_restante * -1

                    periodo_pendiente = IdentificadorDePago.objects.filter(
                        simulador_relacionado=simulador, estatus=False).order_by('periodo_a_pagar').first()

                    periodo_pendiente.monto_restante = periodo_pendiente.monto_restante - monto_pagado

                    if (periodo_pendiente.monto_restante <= 0):
                        periodo_pendiente.estatus = True
                        numero_periodos = numero_periodos-1
                        # cambia estado de periodo a pagado y le resto 1 al numero de periodos pendientes

                    periodo_pendiente.save()

            # Redirigir a la misma página
            return redirect('calificaciones_app:estatus_credito')
        else:
            # Manejar caso de formulario no válido
            return render(request, 'calificaciones/creditos-estatus.html', {'form': form})
    
    
    def post(self, request, *args, **kwargs):
        form = RegistroPagosFormManual(request.POST, request.FILES)
        if form.is_valid():
            # Obtener el simulador seleccionado del formulario
            simulador_id = request.POST.get('simulador')
            simulador = RegistroCreditosModel.objects.get(id=simulador_id)

            # Guardar el formulario
            registro_pago = form.save(commit=False)

            # Asignar el simulador al registro de pago
            registro_pago.simulador = simulador
            registro_pago.save()

            # Obtener el monto del pago registrado
            monto_pagado = registro_pago.monto_pagado
            # numero_pago = registro_pago.numero_pago

            # Obtener la corrida financiera del simulador
            # corrida_financiera = self.calcular_corrida_financiera(
            #     simulador.nombre_prestamo.pago_mensual,
            #     simulador.nombre_prestamo.plazo,
            #     simulador.usuario_user.fecha_solicitud
            # )

            # for pago in corrida_financiera:
            #     if pago['numero_pago'] == monto_pagado:
            #         # Actualizar el monto pagado del pago correspondiente
            #         pago['monto_pagado'] = registro_pago.monto_pagado
            #         pago['estado_pago'] = pago['pago_mensual'] - \
            #             registro_pago.monto_pagado
            #         break

            # Guardar la corrida financiera actualizada en el simulador

            simulador.save()
            
             # Obtener el objeto SimuladorPrueba seleccionado del formulario
            simulador = form.cleaned_data['simulador']

            # Obtener el monto pagado del formulario
            monto_pagado = form.cleaned_data['monto_pagado']

            periodos = IdentificadorDePagoRegistroMan.objects.filter(
                simulador_relacionado=simulador, estatus=False)
            # array con los periodos sin pagar
            numero_periodos = len(periodos)

            if (numero_periodos > 0):

                periodo_pendiente = IdentificadorDePagoRegistroMan.objects.filter(
                    simulador_relacionado=simulador, estatus=False).order_by('periodo_a_pagar').first()
                # periodo mas reciente sin pagar

                periodo_pendiente.monto_restante = periodo_pendiente.monto_restante - monto_pagado

                if (periodo_pendiente.monto_restante <= 0):
                    periodo_pendiente.estatus = True
                    numero_periodos = numero_periodos-1
                    # cambia estado de periodo a pagado y le resto 1 al numero de periodos pendientes

                periodo_pendiente.save()
                # guarde la instancia

                while (periodo_pendiente.monto_restante < 0 and numero_periodos > 0):
                    monto_pagado = periodo_pendiente.monto_restante * -1

                    periodo_pendiente = IdentificadorDePagoRegistroMan.objects.filter(
                        simulador_relacionado=simulador, estatus=False).order_by('periodo_a_pagar').first()

                    periodo_pendiente.monto_restante = periodo_pendiente.monto_restante - monto_pagado

                    if (periodo_pendiente.monto_restante <= 0):
                        periodo_pendiente.estatus = True
                        numero_periodos = numero_periodos-1
                        # cambia estado de periodo a pagado y le resto 1 al numero de periodos pendientes

                    periodo_pendiente.save()

            # Redirigir a la misma página
            return redirect('calificaciones_app:estatus_credito')
        
        else:
            # Manejar caso de formulario no válido
            return render(request, 'calificaciones/creditos-estatus.html', {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registro_pagos_form'] = RegistroPagosForm() 
        context['registro_pagos_form_manual'] = RegistroPagosFormManual()
        context['corrida'] =IdentificadorDePago.objects.all()

        return context

    






    
    
class RegistroPagos(CreateView):
    model = RegistroPagosModel
    template_name = 'calificaciones/registro-pagos.html'
    form_class =RegistroPagosForm
    success_url = reverse_lazy('calificaciones_app:registro_pagos')
    #context_object_name = 'registros_pagos'
    
    
    def form_valid(self, form):
        # Obtener el simulador asociado al registro de pago
        simulador = form.cleaned_data['simulador']
        # Obtener el último registro de pago para calcular el número de pago
        ultimo_pago = RegistroPagosModel.objects.filter(simulador=simulador).order_by('-fecha_pago').first()
        numero_pago = 1 if not ultimo_pago else ultimo_pago.numero_pago + 1
        # Calcular el monto restante
        monto_restante = simulador.nombre_prestamo.pago_mensual * numero_pago - form.cleaned_data['monto_pagado']
        # Asignar el número de pago y el monto restante al registro de pago
        form.instance.numero_pago = numero_pago
        form.instance.monto_restante = monto_restante
        return super().form_valid(form)
    
    
    ###### el original
    
    # def form_valid(self, form):
    #     # Asigna el usuario actual al campo "usuario" del formulario
    #     # form.instance.usuario = self.request.user

    #     # Realiza la solicitud AJAX para obtener los datos de EstatusCredito
    #     num_contrato_id = form.cleaned_data['num_contrato'].id
    #     estatus_credito = EstatusCredito.objects.get(pk=num_contrato_id)

    #     # Actualiza los campos del formulario con los datos obtenidos
    #     form.instance.monto_total_registro = estatus_credito.monto_pago_men
        
    #     form.instance.documento = form.cleaned_data['documento']
        
    #     form.save()
    #     # Otros campos que desees actualizar...

    #     return super().form_valid(form)    
 
    
def obtener_monto_total(request):
    if request.method == 'GET':
        num_contrato_id = request.GET.get('num_contrato_id')
        try:
            estatus_credito = SimuladorPrueba.objects.get(id=num_contrato_id)
            monto_total = estatus_credito.nombre_prestamo.pago_mensual
            usuario = estatus_credito.usuario_user.email
            return JsonResponse({'monto_total': monto_total,'usuario': usuario})
        except estatus_credito.DoesNotExist:
            return JsonResponse({'monto_total': None,'usuario': None})
        
# def obtener_monto_total(request):
#     if request.method == 'GET':
#         num_contrato_id = request.GET.get('num_contrato_id')
#         try:
#             estatus_credito = EstatusCredito.objects.get(id=num_contrato_id)
#             monto_total = estatus_credito.monto_pago_men
#             usuario = estatus_credito.cliente_estatus.email
#             return JsonResponse({'monto_total': monto_total,'usuario': usuario})
#         except estatus_credito.DoesNotExist:
#             return JsonResponse({'monto_total': None,'usuario': None})
    
    
#class GetEstatusCreditoDataView(View):
    # def get(self, request, num_contrato, *args, **kwargs):
    #     estatus_credito = get_object_or_404(EstatusCredito, numero_contrato_estatus=num_contrato)
    #     usuario = estatus_credito.cliente_estatus.username
    #     monto_total = estatus_credito.monto_total
    #     # data = {
    #     #     'usuario': estatus_credito.cliente_estatus.username,
    #     #     'monto_total': estatus_credito.monto_total,
    #     # }
    #     return JsonResponse({'usuario': usuario,'monto_total':monto_total})
    
    
# class GetNombreProductoView(View):
#     def get(self, request, prestamo_id, *args, **kwargs):
#         prestamo = get_object_or_404(Prestamo, id=prestamo_id)
#         nombre_producto = prestamo.nombre_producto
#         tipo_prestamo_nombre = prestamo.tipo_prestamo.tipo_credito if prestamo.tipo_prestamo else None
#         return JsonResponse({'nombre_producto': nombre_producto,'tipo_prestamo':tipo_prestamo_nombre})
   
   
   
##### corrida financiera #####
""" 
def calcular_corrida_financiera(self, pago_mensual, plazo, fecha_solicitud, monto_pagado=None, frecuencia_pago='semanal'):
        detalles_pago = []
        fecha_actual = fecha_solicitud
        # index_pago_registrado = 0
        monto_restante = pago_mensual * plazo

        numero_pago = 1

        if fecha_actual is None:
            # Asigna la fecha actual si no hay fecha de solicitud
            fecha_actual = timezone.now().date()

        # for numero_pago in range(1, plazo + 1):
            detalle_pago = {
                'numero_pago': numero_pago,
                'fecha_pago': fecha_actual,
                'pago_mensual': pago_mensual
            }
            # # Si es el primer pago y se proporciona el monto pagado, establecerlo
            # numero_pago == numero_pago and
            if monto_pagado is not None:
                # if monto_pagado is not None and index_pago_registrado < numero_pago:
                # index_pago_registrado += 1

                monto_a_pagar = min(monto_pagado, monto_restante)
                detalle_pago['monto_pagado'] = monto_a_pagar
                monto_restante -= monto_a_pagar

                diferencia = pago_mensual - monto_a_pagar

                detalle_pago['diferencia_pago'] = diferencia

                if diferencia == 0 or monto_a_pagar == 0:
                    detalle_pago['estado_pago'] = 0
                else:
                    detalle_pago['estado_pago'] = diferencia

                if diferencia < 0:
                    numero_pago += 1
                    monto_pagado = diferencia * -1
                    self.calcular_corrida_financiera(
                        pago_mensual, plazo, fecha_solicitud, monto_pagado, frecuencia_pago='semanal')

                # index_pago_registrado += 1

            detalles_pago.append(detalle_pago)
            # Actualizar la fecha para el próximo pago según la frecuencia de pago
            if frecuencia_pago == 'semanal':
                fecha_actual += timedelta(days=7)
            elif frecuencia_pago == 'mensual':
                # Suponiendo meses de 30 días para simplificar
                fecha_actual += timedelta(days=30)

        return detalles_pago
"""


"""
                # Obtener el objeto SimuladorPrueba seleccionado del formulario
            simulador = form.cleaned_data['simulador']

            # Obtener el monto pagado del formulario
            monto_pagado = form.cleaned_data['monto_pagado']

            periodo_pendiente = IdentificadorDePago.objects.filter(
                simulador_relacionado=simulador, estatus=False).order_by('periodo_a_pagar').first()

            periodo_pendiente.monto_restante = periodo_pendiente.monto_restante - monto_pagado

            periodo_pendiente.save()
"""
    
    
    
         
        
    
    
    
    
    
    
