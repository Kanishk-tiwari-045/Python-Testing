from django.urls import path
from . import views

urlpatterns = [
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
]