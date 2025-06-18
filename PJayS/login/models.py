from django.db import models
import uuid

# Create your models here.
class Admin(models.Model):
    admin_id = models.CharField(max_length=36, unique=True, blank=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=50 ,null= True)
    Name = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.admin_id:
            self.admin_id = str(uuid.uuid4())
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.username
