from django.urls import path
from frontend_itea.views import base, card, index, load_dates

urlpatterns = [
    path('', base, name='base'),
    path('card', card, name='card'),
    path("index", index, name="index"),
    path("load_dates/", load_dates, name="load_dates"),
]
 


