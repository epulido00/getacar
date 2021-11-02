from django.db import models

from applications.users.models import User

# Create your models here.

class Car(models.Model):

    TRANSMISSION_CHOICES = (
        ('M', 'Manual'),
        ('A', 'Automatico')
    )

    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    year = models.IntegerField()
    type_car = models.CharField(max_length=20)
    transmission = models.CharField(max_length=1, choices=TRANSMISSION_CHOICES, blank=True)
    price = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Auto'
        verbose_name_plural = 'Autos'

    def __str__(self):
        return self.brand + " " + self.model + " " + str(self.year)
