from django.urls import path
from .views import generate_report_pelajar, generate_report_kakitangan, generate_report_saham, generate_report_keseluruhan

urlpatterns = [
    path('generate_report_pelajar/', generate_report_pelajar, name='generate_report_pelajar'),
    path('generate_report_kakitangan/', generate_report_kakitangan, name='generate_report_kakitangan'),
    path('generate_report_saham/', generate_report_saham, name='generate_report_saham'),
    path('generate_report_keseluruhan/', generate_report_keseluruhan, name='generate_report_keseluruhan')
    # path('home/generate_report_view/', generate_report_view, name='generate_report_view'),

]
