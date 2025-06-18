from django import forms
from .models import Teacher

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'nama', 
            'ic_cikgu', 
            'jantina', 
            'alamat_rumah', 
            'pangkat', 
            'ahli', 
            'status',
            'modal_syer', 
            'tarikh_daftar'
        ]

    def clean_ic_cikgu(self):
        ic_cikgu = self.cleaned_data.get('ic_cikgu')
        if Teacher.objects.filter(ic_cikgu=ic_cikgu).exists():
            raise forms.ValidationError("This IC number is already registered. Please use a different one.")
        return ic_cikgu

    def clean_nama(self):
        nama = self.cleaned_data.get('nama')
        if not nama:
            raise forms.ValidationError("Please enter a name.")
        return nama

    # Add similar clean methods for other fields as necessary


class UpdateTeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'nama', 
            'ic_cikgu', 
            'jantina', 
            'alamat_rumah', 
            'pangkat', 
            'ahli', 
            'status',
            'modal_syer', 
            'tarikh_daftar'
        ]
