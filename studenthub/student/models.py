from enum import unique
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
class Student(models.Model):
    cedula = models.CharField(max_length=10, blank=True, null=True, unique=True)
    nombre = models.CharField(max_length=50) #charfield
    edad = models.IntegerField() #integerField
    correo = models.EmailField(max_length= 50, blank=True, unique=True)
    carrera = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10, blank=True, null=True, unique=True)

    creado_en = models.DateTimeField(auto_now_add=True, blank= True, null= True)
    #Registro de la fecha automático

    #Para cargar los nombres de los estudiantes al escogerlos en asignaturas
    def __str__(self):
        return self.nombre

class Asignatura(models.Model):
    estudiante = models.ForeignKey(Student, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=20, unique=True)
    creditos = models.IntegerField(validators=[MinValueValidator(1)])
    semestre = models.CharField(max_length=20, blank=True, null=True)
