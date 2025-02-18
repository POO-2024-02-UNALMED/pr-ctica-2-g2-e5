from baseDatos.Teatro import Teatro
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

    obra1 = Obra(nombre="pepe")
    obra2 = Obra(nombre="dante")
    obra3 = Obra(nombre="labella")
    sala=Sala()
                    
    funcion1 = Funcion(obra=obra1,horario="12:00",sillas=sala.create_sillas(32))
    funcion2 = Funcion(obra=obra1,horario="14:00",sillas=sala.create_sillas(8))
    funcion3 = Funcion(obra=obra1,horario="13:00",sillas=sala.create_sillas(16))

    print("Base de datos reinicializada")