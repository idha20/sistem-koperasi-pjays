from django.urls import path
from .views import *

urlpatterns = [
    path('register_teacher/', register_teacher, name='register_teacher'),
    path('delete_teacher_page/', delete_teacher_page, name='delete_teacher_page'),
    path('delete_teacher/<str:teacher_id>/', delete_teacher, name='delete_teacher'),
    path('update_teacher_page/', update_teacher_page, name='update_teacher_page'),
    path('update_teacher_page/edit_teacher/<str:teacher_id>/', edit_teacher, name='edit_teacher'),
    path('data_teacher/', data_teacher, name='data_teacher'),
]
