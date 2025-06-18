from django.db import models
from teacher.models import Teacher
from student.models import Member
from django.utils import timezone

class SahamTeacher(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_saham_added = models.DateTimeField(default=timezone.now, editable=False)
    note = models.TextField(blank=True, null=True)  # Add a new field for notes

    def __str__(self):
        return f"{self.teacher.nama} - {self.amount}"

class SahamStudent(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_saham_added = models.DateTimeField(default=timezone.now, editable=False)
    note = models.TextField(blank=True, null=True)  # Add a new field for notes

    def __str__(self):
        return f"{self.member.nama} - {self.amount}"