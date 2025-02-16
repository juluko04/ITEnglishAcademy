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

# Función para renderizar el dashboard base
def base(request):

    # Obtener todos los cursos con sus fechas asociadas
    courses = Courses.objects.all()
    precio_cursos = []
    descripcion_cursos = []
    start_dates = []
    end_dates = []

    for course in courses:
        precio_cursos.append(course.price)
        descripcion_cursos.append(course.description)
        end_dates.append(course.end_date)
        start_dates.append(course.start_date)

    precio_1 = int(precio_cursos[0])
    precio_2 = int(precio_cursos[1])
    precio_3 = int(precio_cursos[2])
    precio_4 = int(precio_cursos[3])
    precio_5 = int(precio_cursos[4])
    precio_6 = int(precio_cursos[5])

    descripcion_1 = str(descripcion_cursos[0])
    descripcion_2 = str(descripcion_cursos[1])
    descripcion_3 = str(descripcion_cursos[2])
    descripcion_4 = str(descripcion_cursos[3])
    descripcion_5 = str(descripcion_cursos[4])
    descripcion_6 = str(descripcion_cursos[5])

    start_dates_1 = str(start_dates[0])
    start_dates_2 = str(start_dates[1])
    start_dates_3 = str(start_dates[2])
    start_dates_4 = str(start_dates[3])
    start_dates_5 = str(start_dates[4])
    start_dates_6 = str(start_dates[5])

    end_dates_1 = str(end_dates[0])
    end_dates_2 = str(end_dates[1])
    end_dates_3 = str(end_dates[2])
    end_dates_4 = str(end_dates[3])
    end_dates_5 = str(end_dates[4])
    end_dates_6 = str(end_dates[5]) 

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
            ACCESS_TOKEN = "APP_USR-8417954214906363-021222-a2d936741705b787e9c000d1b98b9018-2264326901"  # Token real de MercadoPago
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
                recipient_list=["julianzakatak@gmail.com"],  # Cambiar al correo deseado
                fail_silently=False
            )

    # Renderizar la plantilla con los niveles y horarios
    return render(request, 'base.html', {"form": form, 'courses_info': courses_info,
        "precio_1": precio_1, "precio_2": precio_2, "precio_3": precio_3, "precio_4": precio_4, "precio_5": precio_5, "precio_6": precio_6,
        "descripcion_1": descripcion_1, "descripcion_2": descripcion_2, "descripcion_3": descripcion_3, "descripcion_4": descripcion_4, "descripcion_5": descripcion_5, "descripcion_6": descripcion_6,
        "start_dates_1": start_dates_1, "start_dates_2": start_dates_2, "start_dates_3": start_dates_3, "start_dates_4": start_dates_4, "start_dates_5": start_dates_5, "start_dates_6": start_dates_6,
        "end_dates_1": end_dates_1, "end_dates_2": end_dates_2, "end_dates_3": end_dates_3, "end_dates_4": end_dates_4, "end_dates_5": end_dates_5, "end_dates_6": end_dates_6
                                         })


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


