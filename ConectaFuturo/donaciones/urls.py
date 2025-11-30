from django.urls import path
from . import views


urlpatterns = [
    path('nueva/', views.realizar_donacion, name='realizar_donacion'),
]