from baseDatos.Teatro import Teatro
from gestorAplicacion.gestionVentas.Cliente import Cliente
from gestorAplicacion.gestionObras.Actor import Actor
from gestorAplicacion.herramientas.Genero import Genero
from gestorAplicacion.gestionFinanciera.CuentaBancaria import CuentaBancaria
from gestorAplicacion.herramientas.Aptitud import Aptitud

def resetMemory():
    Teatro.setInstancia( Teatro() )

    Cliente(id = 426, tipo= "Empresa")

    actor1 = Actor("Pedro Pascal", 10292122)
    genres = [Genero.COMEDIA, Genero.CIRCO]
    actor1.setGeneros(genres)
    actor1.setCalificacion(4.1)
    actor1.setSexo('M')
    actor1.setEdad(49)
    actor1.setCalificacionPorAptitud(Aptitud.IMPROVISACION, 4.2)

    genres.append(Genero.DRAMA)
    actor2 = Actor("Eddie Murphy", 9032723)
    actor2.setGeneros(genres)
    actor2.setCalificacion(3.8)
    actor2.setSexo('M')
    actor2.setEdad(62)

    genres.append(Genero.EXPERIMENTAL)
    actor3 = Actor("Emma Stone", 90234243)
    actor3.setGeneros(genres)
    actor3.setCalificacion(4.6)
    actor3.setSexo('F')
    actor3.setEdad(36)
    actor3.setCalificacionPorAptitud(Aptitud.IMPROVISACION, 4.4)

    genres.append(Genero.FANTASIA)
    actor4 = Actor("Antonio Banderas", 90234263)
    actor4.setGeneros(genres)
    actor4.setCalificacion(4.7)
    actor4.setSexo('M')
    actor4.setEdad(64)
    actor4.setCalificacionPorAptitud(Aptitud.IMPROVISACION, 3.9)

    genres.append(Genero.MUSICAL)
    actor5 = Actor("Samuel L. Jackson", 91234203)
    actor5.setGeneros(genres)
    actor5.setCalificacion(5.0)
    actor5.setSexo('M')
    actor5.setEdad(76)

    genres.append(Genero.ROMANCE)
    actor6 = Actor("Orson Welles", 90230543)
    actor6.setGeneros(genres)
    actor6.setCalificacion(4.2)
    actor6.setSexo('M')
    actor6.setEdad(85)

    genres.append(Genero.TERROR)
    actor7 = Actor("John Travolta", 60234243)
    actor7.setGeneros(genres)
    actor7.setCalificacion(4.5)
    actor7.setSexo('M')
    actor7.setEdad(70)

    actor8 = Actor("Carmen Maura", 90456243)
    actor8.setGeneros(genres)
    actor8.setCalificacion(4.3)
    actor8.setSexo('F')
    actor8.setEdad(79)

    actor9 = Actor("Florina Lemaitre", 9076243)
    actor9.setGeneros(genres)
    actor9.setCalificacion(3.9)
    actor9.setSexo('F')
    actor9.setEdad(36)

    # Creación del cliente Warner
    warner = Cliente(tipo = "Empresa", id = 246,
                     cuenta_bancaria= CuentaBancaria(246, 0))
    warner.getHistorial().append(actor3)
    warner.getCuentaBancaria().ingresar(3_700_000)

    print("Base de datos reinicializada")