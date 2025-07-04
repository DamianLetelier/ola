from django.db import models

class Empleado(models.Model):
    GENEROS = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    edad = models.PositiveIntegerField()
    genero = models.CharField(max_length=1, choices=GENEROS)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='empleados/', null=True, blank=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
