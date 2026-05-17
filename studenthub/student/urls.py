#Path, para crear rutas
from django.urls import path
from . import views

app_name = "student"

urlpatterns = [
    path("",views.home, name="home"),
    path("listar_students/",views.listar_students, name="listar"),
    path("crear_students/",views.crear_students, name="crear"),
    path("editar_students/<int:pk>/",views.editar_students, name="editar"),
    path("eliminar_students/<int:pk>/",views.eliminar_students, name="eliminar"),
    path("listar_asignaturas/", views.listar_asignaturas, name="listar_asignaturas"),
    path("crear_asignaturas/", views.crear_asignaturas, name="crear_asignaturas"),
    path("editar_asignaturas/<int:pk>/", views.editar_asignaturas, name="editar_asignaturas"),
    path("eliminar_asignaturas/<int:pk>/", views.eliminar_asignaturas, name="eliminar_asignaturas"),
]
