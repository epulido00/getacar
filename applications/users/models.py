from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino')
    )

    email = models.EmailField(unique=True)
    nombres = models.CharField(max_length=30, blank = True)
    apellidos = models.CharField(max_length=30, blank = True)
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    telefono = models.CharField(max_length=10, blank=True)
    #
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.email


