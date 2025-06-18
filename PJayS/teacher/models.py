from django.db import models
from django.core.validators import RegexValidator

def generate_teacher_id():
    prefix = "STAFF"
    try:
        last_teacher = Teacher.objects.filter(teacher_id__startswith=prefix).order_by('-teacher_id').first()
        if last_teacher and last_teacher.teacher_id[len(prefix):]:
            last_id_num = int(last_teacher.teacher_id[len(prefix):])
        else:
            last_id_num = 0
    except (ValueError, TypeError) as e:
        print(f"Error in generate_teacher_id: {e}")
        last_id_num = 0

    new_id_num = last_id_num + 1
    new_id = f"{prefix}{new_id_num:04d}"
    print(f"Generated new Teacher ID: {new_id}")
    return new_id

class Teacher(models.Model):
    teacher_id = models.CharField(max_length=9, primary_key=True, editable=False, default=generate_teacher_id)
    nama = models.CharField(max_length=100)
    
    # Validator for ic_cikgu to ensure only numbers and 12 digits
    ic_cikgu = models.CharField(
        max_length=12, 
        unique=True,
        validators=[RegexValidator(r'^\d{12}$', message="IC must be exactly 12 digits")]
    )
    
    status = models.CharField(max_length=50, choices=[('Selesai', 'Selesai'), ('Belum Selesai', 'Belum Selesai')])
    jantina = models.CharField(max_length=10, choices=[('Lelaki', 'Lelaki'), ('Perempuan', 'Perempuan')])
    alamat_rumah = models.CharField(max_length=255)
    pangkat = models.CharField(max_length=50, choices=[('Pengerusi', 'Pengerusi'), 
                                                        ('Naib Pengerusi', 'Naib Pengerusi'), 
                                                        ('Pegawai Ehwal Ekonomi', 'Pegawai Ehwal Ekonomi'), 
                                                        ('Penolong Pegawai Ehwal Ekonomi', 'Penolong Pegawai Ehwal Ekonomi'), 
                                                        ('Juruaudit', 'Juruaudit'), 
                                                        ('Penolong Juruaudit', 'Penolong Juruaudit'), 
                                                        ('Guru Biasa', 'Guru Biasa'), 
                                                        ('Lain-lain', 'Lain-lain')])
    ahli = models.CharField(max_length=11, choices=[('Aktif', 'Aktif'), ('Tidak Aktif', 'Tidak Aktif')], default='Aktif')
    modal_syer = models.DecimalField(max_digits=10, decimal_places=2)
    tarikh_daftar = models.DateField()

    def __str__(self):
        return self.nama
