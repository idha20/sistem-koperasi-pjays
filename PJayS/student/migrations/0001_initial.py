# Generated by Django 5.1.1 on 2024-10-08 06:21

import django.core.validators
import student.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('member_id', models.CharField(default=student.models.generate_member_id, editable=False, max_length=8, primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=100)),
                ('ic_pelajar', models.CharField(max_length=12, unique=True, validators=[django.core.validators.RegexValidator('^\\d{12}$', message='IC must be exactly 12 digits')])),
                ('jantina', models.CharField(choices=[('Lelaki', 'Lelaki'), ('Perempuan', 'Perempuan')], max_length=10)),
                ('kaum', models.CharField(choices=[('-', '-'), ('IBAN ATAU SEA DAYAK', 'IBAN ATAU SEA DAYAK'), ('INDONESIA', 'INDONESIA'), ('KADAZAN', 'KADAZAN'), ('KAYAN', 'KAYAN'), ('MELAYU', 'MELAYU'), ('ORANG ASLI', 'ORANG ASLI'), ('SEMAI', 'SEMAI'), ('THAI', 'THAI'), ('LAIN-LAIN', 'LAIN-LAIN')], max_length=50)),
                ('agama', models.CharField(choices=[('-', '-'), ('BUDDHA', 'BUDDHA'), ('ISLAM', 'ISLAM'), ('KRISTIAN', 'KRISTIAN'), ('TIADA AGAMA', 'TIADA AGAMA'), ('LAIN-LAIN', 'LAIN-LAIN')], max_length=50)),
                ('alamat_rumah', models.CharField(max_length=255)),
                ('tingkatan', models.CharField(choices=[('-', '-'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=50)),
                ('kelas', models.CharField(choices=[('-', '-'), ('ANGGERIK', 'ANGGERIK'), ('CEMPAKA', 'CEMPAKA'), ('DAHLIA', 'DAHLIA'), ('MAWAR', 'MAWAR'), ('SEROJA', 'SEROJA'), ('TERATAI', 'TERATAI'), ('UM', 'UM'), ('UKM', 'UKM'), ('USM', 'USM'), ('LILY', 'LILY')], max_length=50)),
                ('ahli', models.CharField(choices=[('Aktif', 'Aktif'), ('Tidak Aktif', 'Tidak Aktif')], default='Aktif', max_length=11)),
                ('modal_syer', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tarikh_daftar', models.DateField()),
            ],
        ),
    ]
