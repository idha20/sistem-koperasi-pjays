# forms.py
from django import forms
from .models import SahamTeacher

class Teacher_Share(forms.ModelForm):
    class Meta:
        model = SahamTeacher
        fields = ['amount','note']

class Student_Share(forms.ModelForm):
    class Meta:
        model = SahamTeacher
        fields = ['amount','note']