from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from student.models import Member  # Import Member from your student app
from teacher.models import Teacher
import json
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

class CustomPasswordResetView(auth_views.PasswordResetView):
    def get_email_context(self, user):
        context = super().get_email_context(user)
        context['protocol'] = self.request.scheme  # 'http' or 'https'
        context['domain'] = self.request.get_host()  # e.g., 'example.com'
        return context

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'login/password_reset_done.html'  # Your custom done page path


class CustomPasswordResetView(PasswordResetView):
    template_name = 'login/password_reset.html'  # Your password reset template path
    email_template_name = 'login/password_reset_email.html'  # Your email template path
    subject_template_name = 'login/password_reset_subject.txt'  # Your subject template path
    success_url = reverse_lazy('password_reset_done')  # Redirect after successful reset

    def form_valid(self, form):
        # You can add custom logic here if needed
        print("Password reset email is being sent.")
        return super().form_valid(form)  # Send the email and redirect to the 'done' page

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'login/password_reset_confirm.html'  # Your custom confirm page path

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'login/password_reset_complete.html'  # Your custom complete page path


def admin_login(request):
    if request.user.is_authenticated:
        return redirect('/home/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_superuser:
                login(request, user)
                return redirect('/home/')
            else:
                messages.info(request, 'You are not an admin user.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'login/pages-login-signup.html')

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Total counts of members and teachers
    member_count = Member.objects.count()
    teacher_count = Teacher.objects.count()

    # Calculate the number of students and teachers who have completed and not completed their shares
    saham_student_selesai = Member.objects.filter(status='Selesai').count()
    saham_student_belum_selesai = Member.objects.filter(status='Belum Selesai').count()

    saham_teacher_selesai = Teacher.objects.filter(status='Selesai').count()
    saham_teacher_belum_selesai = Teacher.objects.filter(status='Belum Selesai').count()

    # Total modal syer for teachers and members
    teacher_total = Teacher.objects.aggregate(total=Sum('modal_syer'))['total'] or 0
    member_total = Member.objects.aggregate(total=Sum('modal_syer'))['total'] or 0

    # Prepare data for the line chart
    line_chart_data = Member.objects.annotate(month_year=TruncMonth('tarikh_daftar')) \
        .values('month_year') \
        .annotate(total_modal_syer=Sum('modal_syer')) \
        .order_by('month_year')

    line_chart_data_list = list(line_chart_data)
    # Convert Decimal objects to float
    line_chart_data_list = [{'month_year': item['month_year'].strftime('%b %Y'), 'total_modal_syer': float(item['total_modal_syer'])} for item in line_chart_data_list]

    # Prepare data for the combined pie chart
    combined_data = [
        {"value": saham_student_selesai, "name": "Pelajar Selesai"},
        {"value": saham_student_belum_selesai, "name": "Pelajar Belum Selesai"},
        {"value": saham_teacher_selesai, "name": "Guru Selesai"},
        {"value": saham_teacher_belum_selesai, "name": "Guru Belum Selesai"},
    ]

    context = {
        'combined_data': json.dumps(combined_data),
        "member": member_count,
        "teacher": teacher_count,
        "teacher_total": float(teacher_total),
        "member_total": float(member_total),
        "line_chart_data": json.dumps(line_chart_data_list)
    }

    return render(request, 'login/laman utama-papan pemuka analisis.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

