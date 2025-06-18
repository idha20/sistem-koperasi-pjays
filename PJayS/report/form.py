from django import forms
from .models import Report

class Report(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            'nama', 
            'ic_pelajar', 
            'jantina', 
            'kaum', 
            'agama', 
            'alamat_rumah', 
            'tingkatan', 
            'kelas', 
            'ahli', 
            'modal_syer', 
            'tarikh_daftar'
        ]