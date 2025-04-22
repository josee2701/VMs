from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User (AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('client', 'Cliente'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username


class VirtualMachine(models.Model):
    name    = models.CharField(max_length=100)
    cores   = models.PositiveSmallIntegerField()
    ram     = models.PositiveIntegerField(help_text="MB")
    disk    = models.PositiveIntegerField(help_text="GB")
    os      = models.CharField(max_length=50)
    status  = models.CharField(max_length=20, choices=(('running','Running'),('stopped','Stopped')))
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.id})"