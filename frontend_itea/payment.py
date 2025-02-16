from django.shortcuts import render
import mercadopago

def payment_mp(request):
    # Credenciales de MercadoPago
    ACCESS_TOKEN = "APP_USR-8417954214906363-021222-a2d936741705b787e9c000d1b98b9018-2264326901"  # Reemplázalo con tu token real

    # Inicializa el SDK de MercadoPago
    sdk = mercadopago.SDK(ACCESS_TOKEN)

    # Datos de la preferencia de pago
    preference_data = {
        "items": [
            {
                "title": "Producto de prueba",
                "quantity": 1,
                "unit_price": 1.0,
                "currency_id": "ARS"
            }
        ]
    }

    # Crear preferencia de pago
    try:
        preference_response = sdk.preference().create(preference_data)
        preference_id = preference_response["response"].get("id", "")
        print(f"Preferencia de pago creada con ID: {preference_id}")
    except Exception as e:
        print(f"Error al crear la preferencia de pago: {e}")
        preference_id = None

    # Pasar el preference_id al template
    return render(request, 'base_login.html', {"preference_id": preference_id})
