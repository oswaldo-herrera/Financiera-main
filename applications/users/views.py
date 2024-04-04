from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.urls import reverse_lazy,reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from allauth.account.views import SignupView
import pandas as pd
import base64
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail,BadHeaderError
import os
from django.conf import settings
from django.views.generic.edit import FormView
from django.views.generic import View,TemplateView,ListView,UpdateView,CreateView,DeleteView
from applications.dashboard.models import ProductoCreditoGrupal,Simulador
from applications.dashboard.forms import SimuladorForm
from .mixins import ValidarPermisosMixin
from .models import User,Ubicacion,CorreosCreditoGrupal,GrupoCreditoPersonal,RegistroCreditosModel
from .forms import UserCreationForm,UserChangeForm,CorreoGrupoCredito,FormularioGRupoCreditoPersona,AdminUserCreationForm,RegistroCreditoForm,UploadExcelForm
import apimarket
import uuid


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Create your views here.


class AdminRegisterView(FormView):
    template_name = 'users/listar-usuarios.html'
    form_class = AdminUserCreationForm
    success_url = reverse_lazy('lista_usuarios')

    def form_valid(self, form):
        # Guardar el formulario y redirigir al éxito si es válido
        form.save()
        return super().form_valid(form)

# def admin_register_view(request):
#     if request.method ==  'POST':
#         form = AdminUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('lista_usuarios')
#         else:
#             form = AdminUserCreationForm()
#         return render(request,'users/listar-usuarios.html',{'form':form})

class RegistrarUsuario(CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        # Obtenemos los datos del formulario
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']  # Obtenemos la contraseña

        # Creamos una instancia del modelo de usuario pero no la guardamos aún
        user = form.save(commit=False)
        # Usamos make_password para cifrar la contraseña antes de guardarla
        user.password = make_password(password)
        user.save()
        return super().form_valid(form)
    
    
def guardar_ubicacion(request):
    if request.method == 'POST':
        latitud = request.POST.get('latitud')  # Obtén estos valores del request POST
        longitud = request.POST.get('longitud')

        # Aquí puedes guardar la ubicación en la base de datos o realizar acciones necesarias
        
        Ubicacion.objects.create(latitud=latitud, longitud=longitud)
        
        return JsonResponse({'mensaje': 'Ubicación recibida correctamente.'})
    else:
        return JsonResponse({'mensaje': 'Solicitud no válida.'}, status=400)
    
class EditarUsuario(UpdateView):
    model = User
    template_name = 'users/editar-usuario.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('user_app:lista_usuarios')
    
    
    
class EliminarUsuarios(DeleteView):
    model = User
    template_name = 'users/eliminar-usuario.html'
    success_url = reverse_lazy('user_app:lista_usuarios')
    
class ListaUsuarios(FormView,ListView):
    template_name = 'users/listar-usuarios.html'
    context_object_name = 'lista'
    form_class = AdminUserCreationForm
    success_url = reverse_lazy('user_app:lista_usuarios')

    def get_queryset(self):
        listar = User.objects.all().order_by('-date_joined')
        return listar
    
    def form_valid(self, form):
        # Guardar el formulario y redirigir al éxito si es válido
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
    
    
# class ListaUsuarios(ListView):
#     template_name = 'users/listar-usuarios.html'
#     context_object_name = 'lista'

#     def get_queryset(self):
#         listar = User.objects.all()
#         return listar
    
    
class SolicitudCheck(View):
    def post(self,request,user_id):
        try:
            user= User.objects.get(pk=user_id)
            user.solicitud = True
            user.save()
            return JsonResponse({'message': 'Solicitud marcada como true'})
        
        except User.DoesNotExist:
            return JsonResponse({'message': 'Solicitud no encontrada'}, status=404)
        
class ClientesAll(ListView):
    template_name = 'users/clientes.html'
    context_object_name = 'clientes'
    
    def get_queryset(self):
        
        cliente = User.objects.filter(solicitud=True)
            
        return cliente
        
        
# def crear_o_vincular_grupos_credito(correos, correos_credito):
#     for correo in correos:
#         grupo_credito_existente = GrupoCreditoPersonal.objects.filter(email=correo).first()

#         if grupo_credito_existente:
#             # Si existe, vincular este CorreosCreditoGrupal al GrupoCreditoPersonal existente
#             grupo_credito_existente.correos_credito = correos_credito
#             grupo_credito_existente.save()
#         else:
#             # Si no existe, crear un nuevo GrupoCreditoPersonal y vincularlo
#             nuevo_grupo_credito = GrupoCreditoPersonal(email=correo, correos_credito=correos_credito)
#             nuevo_grupo_credito.save()
    
class GrupalCredito(SignupView):
    
    template_name = 'users/credito-grupal.html'
    
    def get(self, request, *args, **kwargs):
        signup_form = self.get_form()
        correo_form = CorreoGrupoCredito()
        return render(request, self.template_name, {'signup_form': signup_form, 'correo_form': correo_form})
    
def correo_grupo_credito(request):
    
    if request.method == 'POST':
        
        nombres = request.POST.get('names_grupal')
        apellidos = request.POST.get('surnames_grupal')
        curp = request.POST.get('curp_texto_grupal')
        rfc = request.POST.get('rfc_grupal')
        celular = request.POST.get('celular_coordinador')  
        correo_coordinador = request.POST.get('correo_coordinador')
        participantes_id = request.POST.get('participantes_numero')  
        try:
           
            participantes = ProductoCreditoGrupal.objects.get(pk=participantes_id)
        except ProductoCreditoGrupal.DoesNotExist:
            participantes = None
            
        monto = request.POST.get('monto_vacantes')
        correos_electronicos = []
        
        for key, value in request.POST.items():
            if key.startswith('email_'):
                # Agregar los valores de los campos de correo electrónico a la lista
                correos_electronicos.append(value)
        
        if participantes:
            
            # monto_valor =  ProductoCreditoGrupal() 
            
            correo_nuevo = CorreosCreditoGrupal()
            correo_nuevo.guardar_correos(correos_electronicos,nombres,apellidos,curp,rfc,celular,participantes,monto,correo_coordinador)
            
            
            # Crear un nuevo GrupoCreditoPersonal y asignar los valores
            
            enlace_base = 'http://127.0.0.1:8000/users/formulario-credito/?token={}'
        
            for correo_destinatario in correos_electronicos:
                token = uuid.uuid4().hex  # Generar un token único
                
                nuevo_destinatario = GrupoCreditoPersonal(
                    email=correo_destinatario,
                    token=token,
                    correos_credito=correo_nuevo,
                    
                )
                
                if participantes:
                    
                                    
                    monto_valor, creado = ProductoCreditoGrupal.objects.get_or_create(
                        numero_participante=participantes.numero_participante,
                        defaults={'monto_credito': monto}  # Valores adicionales para la creación
                    )
                
                
                    nuevo_destinatario.productocreditogrupal = monto_valor
                    nuevo_destinatario.save()
                
                    enlace_destinatario = enlace_base.format(token) 
                    
                    mensaje = f'Debes de completar el formulario para unirte al crédito. Visita: {enlace_destinatario}'
                    send_mail(
                        'Credito grupal Yaab',
                        mensaje,
                        settings.EMAIL_HOST_USER,  # Email del remitente configurado en settings.py
                        [correo_destinatario],  # Lista de destinatarios
                        fail_silently=False,
                        
                    )
            
    return redirect('landing_app:landing')
   
    
def obtener_monto(request):
    if request.method == 'GET':
        monto_id = request.GET.get('monto_id')
        try:
            monto = ProductoCreditoGrupal.objects.get(id=monto_id)
            interest = monto.monto_credito
            return JsonResponse({'interest': interest})
        except ProductoCreditoGrupal.DoesNotExist:
            return JsonResponse({'interest': None})   


class FormularioCreditoGrupal(UpdateView):
    model = GrupoCreditoPersonal
    template_name = 'users/formulario-credito-grupal.html'
    form_class = FormularioGRupoCreditoPersona
    success_url = reverse_lazy('login')
    
    # def form_valid(self,form):
    #     token = self.request.GET.get('token')
    
    def get_object(self, queryset=None):
        token = self.request.GET.get('token')
        print(f"Token recibido: {token}")
        return get_object_or_404(GrupoCreditoPersonal, token=token)
    
    def form_valid(self, form):
        # Guardar los archivos si están presentes en la solicitud
        if self.request.FILES:
            
            ine_file = self.request.FILES.get('documento_ine_grupal')
            if ine_file:
                form.cleaned_data['documento_ine_grupal'] = ine_file
                
            for field_name, file in self.request.FILES.items():
                setattr(form.instance, field_name, file)
                
                
        signature_data = self.request.POST.get('signature', None)
        if signature_data:
            # Guardar la firma en tu modelo GrupoCreditoPersonal
            
            
            ## ultima actualizacion 
            # Convertir la cadena base64 en una imagen
            format, imgstr = signature_data.split(';base64,')  # Separar el encabezado de los datos base64
            ext = format.split('/')[-1]  # Obtener la extensión del archivo
            signature_img = ContentFile(base64.b64decode(imgstr), name=f'{self.object.token}_signature.{ext}')

            # Guardar la imagen en el campo firma_imagen
            form.instance.firma_imagen = signature_img
            form.instance.firma_digital = signature_data  # Limpiar el campo firma_digital, ya que ahora tienes la imagen
            
            
        
        self.object = form.save()
        token = self.object.token

        return super().form_valid(form)
        # response_data = {'message': 'Datos guardados exitosamente.'}
        # return JsonResponse(response_data)
        #return HttpResponseRedirect(reverse('login') + f'?token={token}')
    
    
    
class ModalBruroCredito(TemplateView):
    template_name = 'users/buro-credito-html.html'
    
class AvisoPrivacidadGrupal(TemplateView):
    template_name = 'users/aviso-privacidad-grupal.html'


class RegistrarUsuario(CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
class RegistrarCreditoView(CreateView):
    model = RegistroCreditosModel
    template_name = 'users/registrar-credito.html'
    form_class = RegistroCreditoForm
    success_url = reverse_lazy('user_app:registrar_credito')
    

def create_users_from_excel(file_path):
    # Lee el archivo Excel
    df = pd.read_excel(file_path)

    # Itera sobre las filas del DataFrame
    for index, row in df.iterrows():
        # Crea un usuario utilizando los datos de la fila
        user = User.objects.create(
            email=row['email'],
            username=row['username'],
            password=make_password(row['password']),
            edad=row['edad'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            second_name=row['second_name'],
            fecha_nac=row['fecha_nac'],
            curp_texto=row['curp_texto'],
            rfc=row['rfc'],
            estado_civil=row['estado_civil'],
            genero=row['genero'],
            nacionalidad=row['nacionalidad'],
            pais=row['pais'],
            numero_dependientes=row['numero_dependientes'],
            telefono_particular=row['telefono_particular'],
            calle_numero=row['calle_numero'],
            colonia=row['colonia'],
            cp=row['cp'],
            ciudad=row['ciudad'],
            estado_direccion=row['estado_direccion'],
            tipo_vivienda=row['tipo_vivienda'],
            años_radicando=row['años_radicando'],
            conyuge_pareja=row['conyuge_pareja'],
            trabajo_conyuge=row['trabajo_conyuge'],
            antiguedad_laboral_conyuge=row['antiguedad_laboral_conyuge'],
            telefono_conyuge=row['telefono_conyuge'],
            referencia_personal_conyuge_1=row['referencia_personal_conyuge_1'],
            telefono_ref_conyuge_1=row['telefono_ref_conyuge_1'],
            referencia_personal_conyuge_2=row['referencia_personal_conyuge_2'],
            telefono_ref_conyuge_2=row['telefono_ref_conyuge_2'],
            nombre_negocio=row['nombre_negocio'],
            giro=row['giro'],
            inmueble=row['inmueble'],
            años_antiguedad=row['años_antiguedad'],
            calle_numero_negocio=row['calle_numero_negocio'],
            colonia_negocio=row['colonia_negocio'],
            cp_negocio=row['cp_negocio'],
            ciudad_negocio=row['ciudad_negocio'],
            estado_negocio=row['estado_negocio'],
            nombre_aval=row['nombre_aval'],
            primer_apellido=row['primer_apellido'],
            segundo_apellido=row['segundo_apellido'],
            fecha_nac_aval=row['fecha_nac_aval'],
            genero_aval=row['genero_aval'],
            ciudad_aval=row['ciudad_aval'],
            estado_aval=row['estado_aval'],
            rfc_aval=row['rfc_aval'],
            calle_numero_aval=row['calle_numero_aval'],
            colonia_aval=row['colonia_aval'],
            cp_aval=row['cp_aval'],
            relacion_titular=row['relacion_titular'],
            tipo_vivienda_aval=row['tipo_vivienda_aval'],
            lugar_trabajo_aval=row['lugar_trabajo_aval'],
            antiguedad_trabajo_aval=row['antiguedad_trabajo_aval'],
            celular_aval=row['celular_aval'],
            email_aval=row['email_aval'],
            telefono_laboral_aval=row['telefono_laboral_aval'],
            
            # Añade otros campos según sea necesario
        )
        # Guarda el usuario en la base de datos
        user.save()
        
        
        
def upload_excel_view(request):
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            # Procesa el archivo Excel
            create_users_from_excel(excel_file)
            # Redirige a alguna página de éxito o renderiza una plantilla de éxito
            return redirect('user_app:lista_usuarios')
    else:
        form = UploadExcelForm()
    return render(request, 'users/upload_excel.html', {'form': form})
        
# fields = ('email','username','password1','password2','validate_email')

# def upload_excel_view(request):
#     if request.method == 'POST' and request.FILES['excel_file']:
#         excel_file = request.FILES['excel_file']
#         try:
#             # Lee el archivo Excel especificando el motor ('openpyxl' o 'xlrd')
#             df = pd.read_excel(excel_file, engine='openpyxl')
#             # Procesa el DataFrame como necesites
#             # Por ejemplo, itera sobre las filas del DataFrame
#             for index, row in df.iterrows():
#                 # Procesa cada fila como desees
#                 pass
#             # Redirige a alguna página de éxito si es necesario
#             return HttpResponse('El archivo Excel se ha procesado correctamente.')
#         except Exception as e:
#             # Maneja cualquier excepción que pueda ocurrir durante la lectura del archivo Excel
#             return HttpResponse(f'Ocurrió un error al procesar el archivo Excel: {str(e)}')

#     return render(request, 'users/upload_excel.html')

       
    
 
 
 
# def tu_vista_crear_simulador(request,user_id):
    
#     usuario_actual = User.objects.get(pk=user_id)
    
#     if request.method == 'POST':
        
#         formulario = SimuladorForm(request.POST)
#         if formulario.is_valid():
#             simulador = Simulador.objects.create(
#                 tipo_credito=formulario.cleaned_data['tipo_credito'],
#                 plazo_nombre=formulario.cleaned_data['plazo_nombre'],
#                 term=formulario.cleaned_data['term'],
#                 amount=formulario.cleaned_data['amount'],
#                 interest_rate=formulario.cleaned_data['interest_rate'],
#                 monthly_payment=formulario.cleaned_data['monthly_payment']
#             )
            
#             usuario_actual.simulador = simulador
#             usuario_actual.save()
            
#             return redirect('dashboard_app:index')
        
#     else:
            
#         formulario = SimuladorForm()
#     return render(request,'index.html',{'formulario':formulario})
        
        
            
            