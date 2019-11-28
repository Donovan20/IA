from django.urls import path
from app.mentales import views
app_name = 'mentales'

urlpatterns = [
    path('',views.index,name='index'),
    path('diagnostico_general/',views.diagnostico_general,name='diagnosticoG'),
    path('transtornos/',views.transtornos,name='transtornos'),
    path('diagnostico_especifico/',views.diagnostico_especifico,name='diagnosticoE'),
    path('resultado/',views.resultados,name='resultado'),    
]