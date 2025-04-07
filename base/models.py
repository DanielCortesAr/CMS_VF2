from django.db import models
from django.core.validators import FileExtensionValidator
class Vehiculo(models.Model):
    fotografia_vehiculo = models.ImageField(upload_to='fotos/', 
                                            validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    placas = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    año = models.DateField()
    class Meta:
        verbose_name = 'Vehiculo'
        verbose_name_plural = 'Vehiculos'

    def __str__(self):
        return self.placas

