from django import forms
from .models import Student, Asignatura


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["cedula", "nombre", "edad", "correo", "carrera", "telefono"]

    def validar_nombre(self):
        #Traer los datos enviados por el usuario
        nombre = self.cleaned_data["nombre"].strip()
        if len(nombre) == 0:
            raise forms.ValidationError("El campo está vacio")
        return nombre

    def validar_correo(self):
        correo = self.cleaned_data("correo")
        if Student.objects.filter(correo=correo).exists():
            raise forms.ValidationError("Este correo ya está registrado")
        return correo

    def validar_edad(self):
        edad = self.cleaned_data.get("edad")
        if edad is None:
            raise forms.ValidationError("Debes ingresar una edad.")
        if edad <= 0:
            raise forms.ValidationError("La edad debe ser un número positivo.")
        return edad


class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ["estudiante","nombre","codigo","creditos","semestre"]

    def validar_nombre(self):
        #Traer los datos enviados por el usuario
        nombre = self.cleaned_data["nombre"].strip()
        if len(nombre) == 0:
            raise forms.ValidationError("El campo está vacio")
        return nombre

    def validar_creditos(self):
        creditos = self.cleaned_data["creditos"].strip()
        if creditos <= 0:
            raise forms.ValidationError("El campo no puede estar vacio")
        return creditos


