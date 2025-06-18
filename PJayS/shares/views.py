import json
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from .form import Teacher_Share, Student_Share
from .models import Teacher, SahamTeacher, Member, SahamStudent
from student.models import Member
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def share_page(request):
    # pie chart
    teacher_total = sum([teacher.modal_syer for teacher in Teacher.objects.all()])
    member_total = sum([member.modal_syer for member in Member.objects.all()])

    # Prepare the data for the bar chart
    bar_chart_data = Member.objects.values('tingkatan').annotate(total_saham=Sum('modal_syer')).order_by('tingkatan')
    bar_chart_data_list = list(bar_chart_data)
    # Convert Decimal objects to float
    bar_chart_data_list = [{'tingkatan': item['tingkatan'], 'total_saham': float(item['total_saham'])} for item in bar_chart_data_list]

    # Prepare the data for the line chart
    line_chart_data = Member.objects.annotate(month_year=TruncMonth('tarikh_daftar')).values('month_year').annotate(total_modal_syer=Sum('modal_syer')).order_by('month_year')
    line_chart_data_list = list(line_chart_data)
    # Convert Decimal objects to float
    line_chart_data_list = [{'month_year': item['month_year'].strftime('%b %Y'), 'total_modal_syer': float(item['total_modal_syer'])} for item in line_chart_data_list]

    context = {
        "teacher_total": teacher_total,
        "member_total": member_total,
        "teacher" : Teacher.objects.all(),
        "member" : Member.objects.all(),
        "bar_chart_data": json.dumps(bar_chart_data_list),
        "line_chart_data": json.dumps(line_chart_data_list)
    }

    return render(request, 'saham/muka surat-saham komuniti.html', context)

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# function go to page tambah saham teacher
def page_tambah_saham_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    form = SahamTeacher()  # Define an empty form
    return render(request, 'saham/tambah-saham-kakitangan.html', {'form': form, 'teacher': teacher})

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# function add teacher saham into each account
def add_share_teacher_func(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)

    if request.method == 'POST':
        form = Teacher_Share(request.POST)
        if form.is_valid():
            new_modal_syer = form.cleaned_data['amount']
            note_text = form.cleaned_data['note']

            # Update the Teacher model
            teacher.modal_syer += new_modal_syer  # Corrected line - Only add the new amount
            teacher.save()

            # Create a new SahamTeacher record
            SahamTeacher.objects.create(teacher=teacher, amount=new_modal_syer, note=note_text)

            messages.success(request, 'Share amount updated successfully.')
            return redirect('view_account_teacher', teacher_id=teacher_id)  # Pass the teacher_id to the redirect
        else:
            messages.error(request, f"There was an error adding share: {form.errors}")

        # Check if 'kembali' button was pressed
        if 'kembali' in request.POST:
            return HttpResponseRedirect(reverse('view_account_teacher', args=[teacher_id]))

    # If the request method is not POST, redirect back to the form page
    return redirect('page_tambah_saham_teacher', teacher_id=teacher_id)

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# function go to page tambah saham student
def page_tambah_saham_student(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    form = SahamStudent()  # Define an empty form
    return render(request, 'saham/tambah-saham-pelajar.html', {'form': form, 'member': member})

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# function add student saham into each account
def add_share_student_func(request, member_id):
    member = get_object_or_404(Member, pk=member_id)

    if request.method == 'POST':
        form = Student_Share(request.POST)
        if form.is_valid():
            new_modal_syer = form.cleaned_data['amount']
            note_text = form.cleaned_data['note']

            # Update the Teacher model
            member.modal_syer += new_modal_syer  # Corrected line - Only add the new amount
            member.save()

            # Create a new SahamTeacher record
            SahamStudent.objects.create(member=member, amount=new_modal_syer, note=note_text)

            messages.success(request, 'Share amount updated successfully.')
            return redirect('view_account_student', member_id=member_id)
        else:
            messages.error(request, f"There was an error adding share: {form.errors}")

        # Check if 'kembali' button was pressed
        if 'kembali' in request.POST:
            return HttpResponseRedirect(reverse('view_account_student', args=[member_id]))

    return redirect('page_tambah_saham_student', member_id=member_id)

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# view account saham teacher
def view_account_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    saham = SahamTeacher.objects.filter(teacher_id=teacher_id)

    if request.method == 'POST':
        if 'kembali' in request.POST:
            return HttpResponseRedirect(reverse('share_page'))  # Redirect to share_page
        # Handle other form submissions
    return render(request, 'saham/muka surat-lihat saham kakitangan.html', {'teacher': teacher, 'saham': saham})

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# view account saham student
def view_account_student(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    saham = SahamStudent.objects.filter(member_id=member_id)

    if request.method == 'POST':
        if 'kembali' in request.POST:
            return HttpResponseRedirect(reverse('share_page'))  # Redirect to share_page
        # Handle other form submissions
    return render(request, 'saham/muka surat-lihat saham pelajar.html', {'member': member, 'saham': saham})

def pulangan_saham_page(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    saham = SahamTeacher.objects.filter(teacher_id=teacher_id)
    return render(request, 'saham/muka surat-pulangan saham.html', {'teacher': teacher, 'saham': saham})

def pulangan_saham_func(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    saham = SahamTeacher.objects.filter(teacher_id=teacher_id)

    if request.method == 'POST':
        if 'kembali' in request.POST:
            return HttpResponseRedirect(reverse('share_page'))  # Redirect to share_page
        # Handle other form submissions
    return render(request, 'saham/pemulangan-saham-kakitangan.html', {'teacher': teacher, 'saham': saham})