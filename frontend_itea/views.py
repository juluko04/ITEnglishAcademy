# Importaciones necesarias
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
import mercadopago
import json
import os
from django.conf import settings
from .forms import CourseForm
from .models import Dates, Courses

from dotenv import load_dotenv

import os

# Cargar variables del archivo .env
load_dotenv()


# Función para renderizar el dashboard base
def base(request):

    # Obtener todos los cursos con sus fechas asociadas
    courses_og = Courses.objects.all()

    # Procesar cada curso para dividir `unitys`
    for course in courses_og:
        course.unitys_list = course.unitys.split("/")

    # Ruta relativa al directorio de tu proyecto
    courses_file_path = os.path.join(settings.BASE_DIR, 'frontend_itea/web_data/courses.json')

    courses_info = []
    
    # Obtener todos los cursos con sus fechas asociadas
    courses = Courses.objects.all()
    for course in courses:
        dates = Dates.objects.filter(courses=course)  # Obtener las fechas asociadas al curso
        for date in dates:
            courses_info.append({
                "name": course.name,
                "description": course.description,
                "price": course.price,
                "start_date": date.start_date,
                "end_date": date.end_date
            })
    
    # Leer el archivo JSON
    with open(courses_file_path, 'r') as file:
        courses = json.load(file)

    form = CourseForm()

    # Procesar el formulario según el tipo
    if request.method == "POST":
        form_type = request.POST.get('form_type')
        form = CourseForm(request.POST)
        
        if form_type == "inscripcion":
            # Datos del formulario de inscripción
            nombre = request.POST.get('nombre')
            correo = request.POST.get('correo')
            telefono = request.POST.get('telefono')
            fecha_seleccionada = request.POST.get('date')
            nivel_interes = request.POST.get('name')
            situacion_laboral = request.POST.get('situacionLaboral')
            empresa = request.POST.get('empresa', '')
            linkedin = request.POST.get('linkedin', '')

            print(f'nivel_interes {nivel_interes}')

            obtener_data = Courses.objects.filter(id=nivel_interes).first()

            obtener_data_date = Dates.objects.filter(id=fecha_seleccionada).first()



            # Enviar correo de confirmación
            mensaje = f"""
            Nueva inscripción:

            Nombre: {nombre}
            Correo: {correo}
            Teléfono: {telefono}
            Fecha seleccionada: {obtener_data_date.date_name}
            Nivel de interés: {obtener_data.name}
            Situación laboral: {situacion_laboral}
            Empresa: {empresa}
            LinkedIn: {linkedin}
            """
            send_mail(
                subject="Nueva Inscripción",
                message=mensaje,
                from_email="julianzakatak@gmail.com",
                recipient_list=["julianzakatak@gmail.com"],  # Cambiar al correo deseado
                fail_silently=False
            )

            # **Integración con MercadoPago**
            ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
            sdk = mercadopago.SDK(ACCESS_TOKEN)



            preference_data = {
                "items": [
                    {
                        "title": "Inscripción al curso",
                        "quantity": 1,
                        "unit_price": obtener_data.price,  # Precio en ARS, modificar según corresponda
                        "currency_id": "ARS"
                    }
                ],
                "back_urls": {
                    "success": "http://tusitio.com/pago-exitoso/",  # URL donde se redirige después del pago
                    "failure": "http://tusitio.com/pago-fallido/",
                    "pending": "http://tusitio.com/pago-pendiente/"
                },
                "auto_return": "approved"
            }

            # Crear la preferencia de pago
            try:
                preference_response = sdk.preference().create(preference_data)
                payment_url = preference_response["response"].get("init_point", "")  # URL de MercadoPago
            except Exception as e:
                print(f"Error al crear la preferencia de pago: {e}")
                messages.error(request, "Hubo un error al procesar el pago. Intenta nuevamente.")
                return redirect('inscription')  # Redirige al formulario si falla el pago

            # Redirigir a MercadoPago
            return redirect(payment_url)


        elif form_type == "contacto":
            # Datos del formulario de contacto
            nombre = request.POST.get('nombre')
            correo = request.POST.get('correo')
            telefono = request.POST.get('telefono')
            empresa = request.POST.get('empresa', '')
            consulta = request.POST.get('consulta', '')

            # Procesar contacto (agregar lógica aquí)

            # Enviar correo de confirmación
            mensaje = f"""
            Consulta:

            Nombre: {nombre}
            Correo: {correo}
            Teléfono: {telefono}
            Empresa: {empresa}
            Consulta: {consulta}
            """
            send_mail(
                subject="Consulta",
                message=mensaje,
                from_email="julianzakatak@gmail.com",
                recipient_list="julianzakatak@gmail.com",  # Cambiar al correo deseado
                fail_silently=False
            )

    # Renderizar la plantilla con los niveles y horarios
    return render(request, 'base.html', {"form": form, 'courses_info': courses_info, 'courses_og': courses_og})


def card(request):
    # Obtener todos los cursos con sus fechas asociadas
    return render(request, 'card.html')


##

def index(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data["course"])
            print(form.cleaned_data["dates"])
        else:
            print(form.errors)
    else:
        form = CourseForm()
    return render(request, 'index.html', {"form": form})

def load_dates(request):
    courses_id = request.GET.get("name")  # "name" porque así se llama el campo en el form
    dates = Dates.objects.filter(courses_id=courses_id)  # Filtrar correctamente
    return render(request, "date_options.html", {"dates": dates})


