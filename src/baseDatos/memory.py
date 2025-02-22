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

    sala1 = Sala(numero_sala=1,metros_cuadrados= 100,capacidad= 24)
    sala2 = Sala(numero_sala=2,metros_cuadrados= 200,capacidad= 32)
    sala3 = Sala(numero_sala=3,metros_cuadrados= 50,capacidad= 16)
    sala4 = Sala(numero_sala=4,metros_cuadrados= 150,capacidad= 24)
    
    horarioObra1F = [datetime(year = 2024, month = 1, day = 1, hour = 9, minute = 0), datetime(year = 2024, month = 1, day = 1, hour = 12, minute = 30)]
    horarioObra2F = [datetime(year = 2024, month = 1, day = 1, hour = 15, minute = 0), datetime(year = 2024, month = 1, day = 1, hour = 21, minute = 30)]
    horarioObra3F = [datetime(year = 2024, month = 1, day = 1, hour = 13, minute = 0), datetime(year = 2024, month = 1, day = 1, hour = 22, minute = 30)]
    horarioObra4F = [datetime(year = 2024, month = 1, day = 1, hour = 12, minute = 0), datetime(year = 2024, month = 1, day = 1, hour = 22, minute = 30)]
    horarioObra5F = [datetime(year = 2024, month = 1, day = 1, hour = 16, minute = 0), datetime(year = 2024, month = 1, day = 1, hour = 22, minute = 30)]
    horarioObra6F = [datetime(year = 2024, month = 1, day = 1, hour = 20, minute = 0), datetime(year = 2024, month = 1, day = 1, hour = 23, minute = 59)]
    horarioObra7F = [datetime(year = 2024, month = 1, day = 1, hour = 17, minute = 0), datetime(year = 2024, month = 1, day = 1, hour = 23, minute = 30)]
    horarioObra8F = [datetime(year = 2024, month = 1, day = 1, hour = 10, minute = 0), datetime(year = 2024, month = 1, day = 1, hour = 17, minute = 30)]    
    obraNFI1 = Obra(nombre = "NOTFORITE", genero= Genero.EXPERIMENTAL)
    obraNFI2 = Obra(nombre = "NOTFORITE", genero= Genero.DRAMA)
    obraNFI3 = Obra(nombre = "NOTFORITE", genero= Genero.COMEDIA)
    obraNFI4 = Obra(nombre = "NOTFORITE", genero= Genero.MUSICAL)
    obraNFI5 = Obra(nombre = "NOTFORITE", genero= Genero.FANTASIA)
    obraNFI6 = Obra(nombre = "NOTFORITE", genero= Genero.TERROR)
    obraNFI7 = Obra(nombre = "NOTFORITE", genero= Genero.ROMANCE)
    obraNFI8 = Obra(nombre = "NOTFORITE", genero= Genero.CIRCO)
    obra1F = obraNFI1.setFuncionEstelar(Funcion(obra = obraNFI1, horario = horarioObra1F))
    obra2F = obraNFI2.setFuncionEstelar(Funcion(obra = obraNFI2, horario = horarioObra2F))
    obra3F = obraNFI3.setFuncionEstelar(Funcion(obra = obraNFI3, horario = horarioObra3F))
    obra4F = obraNFI4.setFuncionEstelar(Funcion(obra = obraNFI4, horario = horarioObra4F))
    obra5F = obraNFI5.setFuncionEstelar(Funcion(obra = obraNFI5, horario = horarioObra5F))
    obra6F = obraNFI6.setFuncionEstelar(Funcion(obra = obraNFI6, horario = horarioObra6F))
    obra7F = obraNFI7.setFuncionEstelar(Funcion(obra = obraNFI7, horario = horarioObra7F))
    obra8F = obraNFI8.setFuncionEstelar(Funcion(obra = obraNFI8, horario = horarioObra8F))
    
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

    obra1 = Obra(nombre="El Gran Show", genero=Genero.CIRCO, duracion=timedelta(hours=2, minutes=30, seconds=15))
    obra2 = Obra(nombre="Romeo y Julieta", genero=Genero.DRAMA, duracion=timedelta(hours=3, minutes=0, seconds=0))
    obra3 = Obra(nombre="El Mago de os", genero=Genero.MUSICAL, duracion=timedelta(hours=1, minutes=45, seconds=30))
    obra4 = Obra(nombre="Cars 4", genero=Genero.COMEDIA, duracion=timedelta(hours=2, minutes=20, seconds=10))
    obra5 = Obra(nombre="Pepe el grilo", genero=Genero.DRAMA, duracion=timedelta(hours=2, minutes=50, seconds=5))

    

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
    #funcion3 = Funcion(obra=obra1,horario=(datetime(2025, 2, 19, 14, 30),datetime(2025, 3, 19, 14, 30)),sillas=sala.create_sillas(16), sala = Sala(3))

    funcion1 = Funcion(
    obra=obra1, 
    horario=(datetime(2025, 2, 17, 14, 28), datetime(2025, 2, 17, 16, 58)), 
    sala=sala1
    )

    funcion2 = Funcion(
        obra=obra2, 
        horario=(datetime(2025, 2, 18, 19, 00), datetime(2025, 2, 18, 22, 00)), 
        sala=sala2
    )

    funcion3 = Funcion(
        obra=obra3, 
        horario=(datetime(2025, 2, 19, 16, 30), datetime(2025, 2, 19, 18, 15)), 
        
        sala=sala3
    )

    funcion4 = Funcion(
        obra=obra4, 
        horario=(datetime(2025, 2, 20, 20, 00), datetime(2025, 2, 20, 22, 20)), 
        
        sala=sala4
    )

    print("Base de datos reinicializada")