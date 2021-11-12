from django.contrib import admin
from .models import Car

# Register your models here.

class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'year')

admin.site.register(Car, CarAdmin)
