from django.urls import path
from .views import *

urlpatterns = [
    path('share_page/', share_page, name='share_page'),
    path('share_page/view_account_teacher/<str:teacher_id>/', view_account_teacher, name='view_account_teacher'),
    path('share_page/view_account_teacher/page_tambah_saham_teacher/<str:teacher_id>/', page_tambah_saham_teacher, name='page_tambah_saham_teacher'),
    path('share_page/view_account_teacher/add_share_page_teacher/<str:teacher_id>/', add_share_teacher_func, name='add_share_page_teacher'),
    path('share_page/view_account_student/<str:member_id>/', view_account_student, name='view_account_student'),
    path('share_page/view_account_teacher/page_tambah_saham_student/<str:member_id>/', page_tambah_saham_student, name='page_tambah_saham_student'),
    path('share_page/view_account_student/add_share_page_student/<str:member_id>/', add_share_student_func, name='add_share_page_student'),
    path('share_page/pulangan_saham_page/<str:teacher_id>/', pulangan_saham_page, name='pulangan_saham_page'),
    path('share_page/pulangan_saham_page/pulangan_saham/<str:teacher_id>/', pulangan_saham_func, name='pulangan_saham'),
]
