import pandas as pd
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Member
from .form import TambahStudentForm
from .form import UpdateStudentForm
from django.db import transaction, IntegrityError
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control


def get_all_members():
    """Helper function to get all members."""
    return Member.objects.all().order_by('tingkatan')  # Sorting in ascending order

def get_all_tingkatan():
    """Helper function to get all tingkatan, ordered by tingkatan."""
    return Member.objects.values_list('tingkatan', flat=True).distinct().order_by('tingkatan')

def get_all_kelas():
    """Helper function to get all distinct kelas."""
    return Member.objects.values_list('kelas', flat=True).distinct()

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register_student(request):
    if request.method == 'POST':
        form = TambahStudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data berjaya disimpan.')
            return redirect('register_student')
        else:
            # Kumpul dan paparkan mesej ralat yang lebih mesra
            error_messages = form.errors
            friendly_errors = []
            for field, errors in error_messages.items():
                field_name = form[field].label
                for error in errors:
                    friendly_errors.append(f"{field_name}: {error}")
            if friendly_errors:
                messages.error(request, "Sila betulkan ralat berikut: " + ", ".join(friendly_errors))
    else:
        form = TambahStudentForm()

    # Gunakan fungsi pembantu
    member = get_all_members()
    tingkatan = get_all_tingkatan()
    kelas = get_all_kelas()

    context = {
        'member': member,
        'tingkatan': tingkatan,
        'kelas': kelas,
    }

    return render(request, 'student/muka surat-pelajar-tambah data.html', context)


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register_student_kumpulan_page(request):
    if request.method == 'POST':
        file = request.FILES.get('file_upload')
        if file:
            try:
                # Baca fail Excel ke dalam DataFrame
                df = pd.read_excel(file)
                df.columns = df.columns.str.strip()  # Buang ruang kosong di hujung/awal nama lajur

                # Paparkan nama lajur untuk tujuan penyahpepijatan
                print("Lajur dalam fail yang dimuat naik:", df.columns.tolist())

                # Betulkan sebarang kesalahan ejaan dalam nama lajur
                df = df.rename(columns={"tarikh_dafatr": "tarikh_daftar"})  # Betulkan ejaan salah

                # Tentukan lajur yang diperlukan
                required_columns = [
                    "Ic Pelajar", "Nama", "Jantina", "Alamat Rumah", "Tingkatan", 
                    "Kelas", "Ahli", "Status Pengambilan Saham", "Modal Syer", "Tarikh Daftar"
                ]

                # Semak jika semua lajur diperlukan ada
                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    # Gabungkan lajur yang hilang ke dalam satu mesej ralat
                    missing_columns_str = ', '.join(missing_columns)
                    messages.error(request, f"Fail yang dimuat naik tidak mempunyai lajur berikut: {missing_columns_str}. Sila semak fail dan cuba lagi.")
                    return redirect('register_student_kumpulan_page')

                # Gantikan sebarang nilai NaN atau nilai kosong dengan "-"
                df = df.fillna('-')

                df['Ic Pelajar'] = df['Ic Pelajar'].astype(str).str.replace('.0', '', regex=False).str.strip()
                
                for index, row in df.iterrows():
                    ic_pelajar_value = row.get('Ic Pelajar', '').strip()
                    
                    if not ic_pelajar_value or ic_pelajar_value.lower() == 'nan' or ic_pelajar_value == "-":
                        messages.error(request, f"Baris {index + 1}: IC Pelajar diperlukan dan tidak boleh dibiarkan kosong.")
                        return redirect('register_student_kumpulan_page')

                # Tetapkan nilai lalai 'Status Pengambilan Saham' kepada 'Belum Selesai' jika nilai bukan 'Selesai' atau 'Belum Selesai'
                df['Status Pengambilan Saham'] = df['Status Pengambilan Saham'].apply(lambda x: 'Belum Selesai' if x not in ['Selesai', 'Belum Selesai'] else x)

                # Tetapkan nilai lalai 'Ahli' kepada 'Tidak Aktif' jika nilai bukan 'Aktif' atau 'Tidak Aktif'
                df['Ahli'] = df['Ahli'].apply(lambda x: 'Tidak Aktif' if x not in ['Aktif', 'Tidak Aktif'] else x)

                #  Semak jika fail tidak mengandungi data pelajar
                if df.empty:
                    messages.error(request, "Fail yang dimuat naik tidak mengandungi sebarang data pelajar.")
                    return redirect('register_student_kumpulan_page')

                # Tukarkan lajur "Tarikh Daftar" kepada format tarikh yang betul
                def convert_date(value):
                    try:
                        # Semak jika nilai adalah tarikh bersiri Excel (nombor)
                        if isinstance(value, (int, float)):
                            return pd.to_datetime("1899-12-30") + pd.to_timedelta(int(value), unit='D')
                        # Jika bukan, cuba parse sebagai tarikh biasa
                        return pd.to_datetime(value).date()
                    except Exception:
                        return None  # Kembalikan None jika tarikh tidak sah

                # Gunakan fungsi penukaran tarikh dan semak tarikh tidak sah
                df['Tarikh Daftar'] = df['Tarikh Daftar'].apply(convert_date)
                if df['Tarikh Daftar'].isnull().any():
                    messages.error(request, "Beberapa tarikh dalam lajur 'Tarikh Daftar' tidak dapat ditukar. Sila pastikan semua tarikh adalah sah dan cuba lagi.")
                    return redirect('register_student_kumpulan_page')

                # Gunakan transaksi untuk memastikan data disimpan secara atomik
                with transaction.atomic():
                    for index, row in df.iterrows():
                        try:
                            Member.objects.create(
                                ic_pelajar=row.get('Ic Pelajar'),
                                nama=row.get('Nama'),
                                jantina=row.get('Jantina'),
                                status=row.get('Status Pengambilan Saham'),
                                alamat_rumah=row.get('Alamat Rumah'),
                                tingkatan=row.get('Tingkatan'),
                                kelas=row.get('Kelas'),
                                ahli=row.get('Ahli'),
                                modal_syer=row.get('Modal Syer'),
                                tarikh_daftar=row.get('Tarikh Daftar'),
                            )
                        except IntegrityError:
                            messages.error(request, f"Ralat di baris {index + 1}: Pelajar dengan IC {row.get('Ic Pelajar')} sudah wujud. Pendaftaran berganda tidak dibenarkan.")
                            return redirect('register_student_kumpulan_page')
                        
                # Success message after all data is saved
                messages.success(request, "Data pelajar berjaya dimuat naik dan disimpan.")
                return redirect('register_student_kumpulan_page')


            except Exception as e:
                # Mesej ralat umum untuk ralat tidak dijangka
                messages.error(request, "Ralat yang tidak dijangka berlaku semasa memproses fail. Sila semak format dan data fail seperti IC pelajar, kemudian cuba lagi.")
        else:
            messages.error(request, 'Sila pilih fail untuk dimuat naik.')

    # Muatkan semua ahli untuk dipaparkan di halaman
    member = get_all_members()
    return render(request, 'student/muka surat-pelajar-tambah data-kumpulan.html', {'member': member})


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_student_page(request):
    if request.method == 'POST':
        selected_students = request.POST.getlist('selected_students[]')
        if selected_students:
            Member.objects.filter(member_id__in=selected_students).delete()
            messages.success(request, 'Pelajar yang dipilih telah berjaya dipadam.')
        else:
            messages.warning(request, 'Sila pilih sekurang-kurangnya seorang pelajar untuk dipadam.')

    member = get_all_members()
    return render(request, 'student/muka surat-pelajar-padam data.html', {'member': member})

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_student_page(request):
    member = get_all_members()
    tingkatan = get_all_tingkatan()
    kelas = get_all_kelas()

    context = {
        'member': member,
        'tingkatan': tingkatan,
        'kelas': kelas,
    }

    return render(request, 'student/muka surat-pelajar-kemas kini data.html', context)

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_student(request, member_id):
    try:
        # Attempt to retrieve the member by ID
        member = Member.objects.get(member_id=member_id)
    except Member.DoesNotExist:
        messages.error(request, 'The selected student does not exist.')
        return redirect('update_student_page')  # Redirect to the update student page

    if request.method == 'POST':
        # Create the form instance with the posted data and the member instance
        form = UpdateStudentForm(request.POST, instance=member)

        if form.is_valid():
            # Check if any changes were made
            if form.has_changed():
                # Save the form only if there are changes
                form.save()
                messages.success(request, 'Student data updated successfully.')
            else:
                # Notify that no changes were made
                messages.warning(request, 'No updates have been done as the values were the same.')

            return redirect('update_student_page')  # Redirect after handling the form submission
        else:
            # If there are form errors, display them to the user
            error_messages = form.errors
            friendly_errors = []
            for field, errors in error_messages.items():
                field_name = form[field].label
                for error in errors:
                    friendly_errors.append(f"{field_name}: {error}")
            if friendly_errors:
                messages.error(request, "Please correct the following errors: " + ", ".join(friendly_errors))
    else:
        # If not a POST request, create a form instance with the current member data
        form = UpdateStudentForm(instance=member)

    return render(request, 'student/update-page.html', {'form': form, 'member': member})

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_student_kumpulan_page(request):
    if request.method == 'POST':
        new_tingkatan = request.POST.get('new_tingkatan')
        new_kelas = request.POST.get('new_kelas')
        new_status = request.POST.get('new_status')
        new_ahli = request.POST.get('new_ahli')

        selected_students = request.POST.getlist('selected_students[]')

        if selected_students:
            students_to_update = Member.objects.filter(member_id__in=selected_students)

            updated = False

            if new_tingkatan and students_to_update.exclude(tingkatan=new_tingkatan).exists():
                students_to_update.update(tingkatan=new_tingkatan)
                updated = True

            if new_kelas and students_to_update.exclude(kelas=new_kelas).exists():
                students_to_update.update(kelas=new_kelas)
                updated = True

            if new_status and students_to_update.exclude(status=new_status).exists():
                students_to_update.update(status=new_status)
                updated = True

            if new_ahli and students_to_update.exclude(ahli=new_ahli).exists():
                students_to_update.update(ahli=new_ahli)
                updated = True

            if updated:
                messages.success(request, 'Selected students have been updated.')
            else:
                messages.warning(request, 'No updates were made as the values were the same.')
        else:
            messages.warning(request, 'No students selected for updating.')

        return redirect('update_student_kumpulan_page')

    member = get_all_members()

    return render(request, 'student/muka surat-pelajar-kemas kini-kumpulan.html', {'member': member})

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def help_page(request):
    member = Member.objects.all()
    return render(request, 'student/laman-perlukan bantuan.html', {'member': member})

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile_page(request):
    member = Member.objects.all()
    return render(request, 'student/laman-profil.html', {'member': member})

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def data_student(request):
    # list all member
    member =  Member.objects.all()

    # total_student
    total_member = Member.objects.count()

    # total_saham
    total_saham_member = sum([member.modal_syer for member in Member.objects.all()])

    # Calculate total number of active and inactive students
    pelajar_aktif = Member.objects.filter(ahli="Aktif").count()
    pelajar_tidak_aktif = Member.objects.filter(ahli="Tidak Aktif").count()

    # Calculate total number of active and inactive share ownership
    saham_selesai = Member.objects.filter(status="Selesai").count()
    saham_belum_selesai = Member.objects.filter(status="Belum Selesai").count()

    # Prepare the data for the bar chart
    bar_chart_data = Member.objects.values('tingkatan').annotate(total_saham=Sum('modal_syer')).order_by('tingkatan')
    bar_chart_data_list = list(bar_chart_data)
    # Convert Decimal objects to float
    bar_chart_data_list = [{'tingkatan': item['tingkatan'], 'total_saham': float(item['total_saham'])} for item in bar_chart_data_list]

    context = {
        'saham_selesai': saham_selesai,
        'saham_belum_selesai': saham_belum_selesai,
        'pelajar_aktif': pelajar_aktif,
        'pelajar_tidak_aktif' : pelajar_tidak_aktif,
        'member': member,
        'total_saham_member' : total_saham_member,
        'total_member': total_member,
        "bar_chart_data": json.dumps(bar_chart_data_list),
    }
    return render(request, 'student/muka surat data-pelajar & saham.html', context)