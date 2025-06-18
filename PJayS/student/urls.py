from django.urls import path
from .views import register_student, delete_student_page, update_student_page, edit_student, update_student_kumpulan_page, register_student_kumpulan_page, help_page, profile_page, data_student

urlpatterns = [
    path('register_student/', register_student, name='register_student'),
    path('register_student_kumpulan_page/', register_student_kumpulan_page, name='register_student_kumpulan_page'),
    path('delete_student_page/', delete_student_page, name='delete_student_page'),
    path('update_student_page/', update_student_page, name='update_student_page'),
    path('edit_student/<str:member_id>/', edit_student, name='edit_student'),
    path('update_student_kumpulan_page/', update_student_kumpulan_page, name='update_student_kumpulan_page'),
    path('help_page/', help_page, name='help_page'),
    path('profile_page/', profile_page, name='profile_page'),
    path('data_student/', data_student, name='data_student')
]
