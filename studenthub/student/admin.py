from django.contrib import admin
from .models import Student, Asignatura


# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ("cedula","nombre","correo", "carrera",)
    search_fields = ("cedula", "nombre", "correo",)
admin.site.register(Student, StudentAdmin)

class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigo", "creditos", "semestre", "estudiante")
    search_fields = ("nombre", "codigo", )
admin.site.register(Asignatura, AsignaturaAdmin)