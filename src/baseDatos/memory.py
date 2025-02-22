from datetime import datetime, timedelta
from baseDatos.Teatro import Teatro
from gestorAplicacion.gestionClases.Profesor import Profesor
from gestorAplicacion.gestionObras.Obra import Obra
from gestorAplicacion.gestionVentas.Funcion import Funcion
from gestorAplicacion.gestionVentas.Sala import Sala

from gestorAplicacion.gestionVentas.Cliente import Cliente
from gestorAplicacion.gestionObras.Actor import Actor
from gestorAplicacion.herramientas.Genero import Genero
from gestorAplicacion.gestionFinanciera.CuentaBancaria import CuentaBancaria
from gestorAplicacion.herramientas.Aptitud import Aptitud

def resetMemory():
    Teatro.setInstancia( Teatro() )

    Cliente(id = 426, tipo= "Empresa")

    actor1 = Actor("Pedro Pascal", 10292122, 49)
    genres = [Genero.COMEDIA, Genero.CIRCO]
    actor1.setGeneros(genres)
    actor1.setCalificacion(4.1)
    actor1.setSexo("Masculino")
    actor1.setEdad(49)
    actor1.setCalificacionPorAptitud(Aptitud.IMPROVISACION, 4.2)

    genres.append(Genero.DRAMA)
    actor2 = Actor("Eddie Murphy", 9032723, 63)
    actor2.setGeneros(genres)
    actor2.setCalificacion(3.8)
    actor2.setSexo("Masculino")
    actor2.setEdad(62)

    genres.append(Genero.EXPERIMENTAL)
    actor3 = Actor("Emma Stone", 90234243, 36)
    actor3.setGeneros(genres)
    actor3.setCalificacion(4.6)
    actor3.setSexo("Femenino")
    actor3.setEdad(36)
    actor3.setCalificacionPorAptitud(Aptitud.IMPROVISACION, 4.4)

    genres.append(Genero.FANTASIA)
    actor4 = Actor("Antonio Banderas", 90234263, 64)
    actor4.setGeneros(genres)
    actor4.setCalificacion(4.7)
    actor4.setSexo("Masculino")
    actor4.setEdad(64)
    actor4.setCalificacionPorAptitud(Aptitud.IMPROVISACION, 3.9)

    genres.append(Genero.MUSICAL)
    actor5 = Actor("Samuel L. Jackson", 91234203, 76)
    actor5.setGeneros(genres)
    actor5.setCalificacion(5.0)
    actor5.setSexo("Masculino")
    actor5.setEdad(76)

    genres.append(Genero.ROMANCE)
    actor6 = Actor("Orson Welles", 90230543, 70)
    actor6.setGeneros(genres)
    actor6.setCalificacion(4.2)
    actor6.setSexo("Masculino")
    actor6.setEdad(85)

    genres.append(Genero.TERROR)
    actor7 = Actor("John Travolta", 60234243, 70)
    actor7.setGeneros(genres)
    actor7.setCalificacion(4.5)
    actor7.setSexo("Masculino")
    actor7.setEdad(70)

    actor8 = Actor("Carmen Maura", 90456243, 79)
    actor8.setGeneros(genres)
    actor8.setCalificacion(4.3)
    actor8.setSexo("Femenino")
    actor8.setEdad(79)

    actor9 = Actor("Florina Lemaitre", 9076243, 73)
    actor9.setGeneros(genres)
    actor9.setCalificacion(3.9)
    actor9.setSexo("Femenino")
    actor9.setEdad(36)

    # Creación del cliente Warner
    warner = Cliente(tipo = "Empresa", id = 246,
                     cuenta_bancaria= CuentaBancaria(246, 0))
    warner.getHistorial().append(actor3)
    warner.getCuentaBancaria().ingresar(3_700_000)

    obra1 = Obra(nombre="pepe",genero=Genero.CIRCO,duracion = timedelta(hours=2, minutes=30, seconds=15))
    obra2 = Obra(nombre="dante",genero=Genero.CIRCO)
    obra3 = Obra(nombre="labella",genero=Genero.CIRCO)
    sala=Sala()

    Profesor1 = Profesor("Oscar Arango", 1)
    Teatro.getInstancia().getEmpleadosPorRendimiento().append(Profesor1)
    Profesor1.agregar_especializacion(Aptitud.CANTO)
    Profesor2 = Profesor("Danna Valeria", 2)
    Teatro.getInstancia().getEmpleadosPorRendimiento().append(Profesor2)
    Profesor2.agregar_especializacion(Aptitud.CANTO)
    Profesor3 = Profesor("Juan Pablo", 3)
    Teatro.getInstancia().getEmpleadosPorRendimiento().append(Profesor3)
    Profesor3.agregar_especializacion(Aptitud.CANTO)
    Profesor4 = Profesor("Francisco", 4)
    Teatro.getInstancia().getEmpleadosPorRendimiento().append(Profesor4)
    Profesor4.agregar_especializacion(Aptitud.CANTO)
    Profesor5 = Profesor("Miguel Velez", 5)
    Teatro.getInstancia().getEmpleadosPorRendimiento().append(Profesor5)
    Profesor5.agregar_especializacion(Aptitud.CANTO)
    Teatro.getInstancia().getTipoProfesor().append(Profesor1)
    Teatro.getInstancia().getTipoProfesor().append(Profesor2)
    Teatro.getInstancia().getTipoProfesor().append(Profesor3)
    Teatro.getInstancia().getTipoProfesor().append(Profesor4)
    Teatro.getInstancia().getTipoProfesor().append(Profesor5)
    ActorPrueba = Actor("Prueba", 1, 6)
    ActorPrueba.setCalificacionPorAptitud(Aptitud.CANTO, 5.0)
    ActorPrueba.setCalificacionPorAptitud(Aptitud.EMOCIONALIDAD, 5.0)
    ActorPrueba.setCalificacionPorAptitud(Aptitud.BAILE, 5.0)
    ActorPrueba.setCalificacionPorAptitud(Aptitud.IMPROVISACION, 5.0)
    ActorPrueba.setCalificacionPorAptitud(Aptitud.DISCURSO, 5.0)
    sala1=Sala(1)
    sala2=Sala(2)
    sala3=Sala(3)
    sala4=Sala(4)
    sala5=Sala(5)
    sala6=Sala(6)

    funcion1 = Funcion(obra=obra1,horario=(datetime(2025, 2, 17, 14, 30),datetime(2025, 3, 17, 14, 30)),sillas=sala.create_sillas(32), sala= Sala())
    funcion2 = Funcion(obra=obra1,horario=(datetime(2025, 2, 18, 14, 30),datetime(2025, 3, 18, 14, 30)),sillas=sala.create_sillas(8), sala= Sala(2))
    funcion3 = Funcion(obra=obra1,horario=(datetime(2025, 2, 19, 14, 30),datetime(2025, 3, 19, 14, 30)),sillas=sala.create_sillas(16), sala = Sala(3))


    print("Base de datos reinicializada")