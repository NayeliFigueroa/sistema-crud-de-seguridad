from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Asignatura
from .forms import StudentForm, AsignaturaForm
from .auditoria import audit_crud


# Create your views here.
def home(request):
    return redirect("student:listar")

@audit_crud("list", "student")
def listar_students(request):
    #select* from Student
    #Listar todos los registros de estudiante
    estudiantes = Student.objects.all()

    return render(request,"students/listar.html", {"estudiantes":estudiantes})

@audit_crud("create", "student")
def crear_students(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("student:listar") #Ruta URL
    #En caso que el formulario no sea valido, o la peticion sea de tipo GET
    #se muestran los campos del formulario
    return render(request, "students/crear.html", {"form":form})
    #Renderización de la plantilla

@audit_crud("update", "student")
def editar_students(request, pk):
    #Forma 1 de llamar a un registro de estudiante
    estudiante = get_object_or_404(Student, pk=pk)

    form = StudentForm(request.POST or None, instance=estudiante)

    if form.is_valid():
        form.save()
        return redirect("student:listar")

    return render(request, "students/editar.html",
                  {"form":form, "estudiante":estudiante})

@audit_crud("delete", "student")
def eliminar_students(request, pk):
    estudiante = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        estudiante.delete()
        return redirect("student:listar")

    return render(request, "students/eliminar.html",
                  {"estudiante":estudiante})

#Asignaturas
@audit_crud("list", "asignatura")
def listar_asignaturas(request):
    #Listar todos los registros de estudiante
    asignaturas = Asignatura.objects.all()
    return render(request, "asignaturas/listar.html", {"asignaturas": asignaturas})

@audit_crud("create", "asignatura")
def crear_asignaturas(request):
    form = AsignaturaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("student:listar_asignaturas")  # Ruta URL
    # En caso que el formulario no sea valido, o la peticion sea de tipo GET
    # se muestran los campos del formulario
    return render(request, "asignaturas/crear.html", {"form": form})
    # Renderización de la plantilla


@audit_crud("update", "asignatura")
def editar_asignaturas(request, pk):
    # Forma 1 de llamar a un registro de estudiante
    asignaturas = get_object_or_404(Asignatura, pk=pk)

    form = AsignaturaForm(request.POST or None, instance=asignaturas)

    if form.is_valid():
        form.save()
        return redirect("student:listar_asignaturas")

    return render(request, "asignaturas/editar.html",
                  {"form": form, "asignaturas": asignaturas})


@audit_crud("delete", "asignatura")
def eliminar_asignaturas(request, pk):
    asignaturas = get_object_or_404(Asignatura, pk=pk)
    if request.method == "POST":
        asignaturas.delete()
        return redirect("student:listar_asignaturas")

    return render(request, "asignaturas/eliminar_asignaturas.html",
                  {"asignaturas": asignaturas})