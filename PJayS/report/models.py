from django.db import models
from django.core.validators import RegexValidator
from student.models import Member
from teacher.models import Teacher
from django.core.exceptions import ValidationError

class Report(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)  # ForeignKey to Member model
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)  # ForeignKey to Teacher model

    # Personal details
    nama = models.CharField(max_length=100)

    jantina = models.CharField(max_length=10, choices=[('Lelaki', 'Lelaki'), ('Perempuan', 'Perempuan')])

    kaum = models.CharField(max_length=50, choices=[
        ('-', '-'),
        ('IBAN ATAU SEA DAYAK', 'IBAN ATAU SEA DAYAK'),
        ('INDONESIA', 'INDONESIA'),
        ('KADAZAN', 'KADAZAN'),
        ('KAYAN', 'KAYAN'),
        ('MELAYU', 'MELAYU'),
        ('ORANG ASLI', 'ORANG ASLI'),
        ('SEMAI', 'SEMAI'),
        ('THAI', 'THAI'),
        ('LAIN-LAIN', 'LAIN-LAIN')
    ])

    agama = models.CharField(max_length=50, choices=[
        ('-', '-'),
        ('BUDDHA', 'BUDDHA'),
        ('ISLAM', 'ISLAM'),
        ('KRISTIAN', 'KRISTIAN'),
        ('TIADA AGAMA', 'TIADA AGAMA'),
        ('LAIN-LAIN', 'LAIN-LAIN')
    ])

    alamat_rumah = models.CharField(max_length=255)

    tingkatan = models.CharField(max_length=50, choices=[
        ('-', '-'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
    ], null=True, blank=True)

    kelas = models.CharField(max_length=50, choices=[
        ('-', '-'),
        ('ANGGERIK', 'ANGGERIK'),
        ('CEMPAKA', 'CEMPAKA'),
        ('DAHLIA', 'DAHLIA'),
        ('MAWAR', 'MAWAR'),
        ('SEROJA', 'SEROJA'),
        ('TERATAI', 'TERATAI'),
        ('UM', 'UM'),
        ('UKM', 'UKM'),
        ('USM', 'USM'),
        ('LILY', 'LILY')
    ], null=True, blank=True)

    pangkat = models.CharField(max_length=50, choices=[
        ('Pengerusi', 'Pengerusi'),
        ('Naib Pengerusi', 'Naib Pengerusi'),
        ('Pegawai Ehwal Ekonomi', 'Pegawai Ehwal Ekonomi'),
        ('Penolong Pegawai Ehwal Ekonomi', 'Penolong Pegawai Ehwal Ekonomi'),
        ('Juruaudit', 'Juruaudit'),
        ('Penolong Juruaudit', 'Penolong Juruaudit'),
        ('Guru Biasa', 'Guru Biasa'),
        ('Lain-lain', 'Lain-lain')
    ], null=True, blank=True)

    ahli = models.CharField(max_length=11, choices=[('Aktif', 'Aktif'), ('Tidak Aktif', 'Tidak Aktif')], default='Aktif')
    modal_syer = models.DecimalField(max_digits=10, decimal_places=2)
    tarikh_daftar = models.DateField()

    def clean(self):
        if self.member and self.teacher:
            raise ValidationError("A report cannot belong to both a student and a teacher.")
        if not self.member and not self.teacher:
            raise ValidationError("A report must belong to either a student or a teacher.")

    def __str__(self):
        if self.member:
            return f"Pelajar: {self.nama}"
        elif self.teacher:
            return f"Guru: {self.nama}"
        return self.nama
