from gestorAplicacion.gestionObras.Artista import Artista
from baseDatos.Teatro import Teatro
from gestorAplicacion.herramientas.Aptitud import Aptitud

class Actor(Artista):
    TASA = 1_000_000

    def __init__(self, nombre: str, id: int):
        super.__init__(nombre, id)

        self.generos = []
        self.notas = []
        self.reevaluacion = False
        self.precioContrato = None
        
        #segun las aptitudes que estén en el enum
        self.aptitudes = [aptitud.value for aptitud in Aptitud]
        
        #inicializar calificaciones en 0
        self.calificacionesAptitudes = [0] * len(self.aptitudes)

        #lista de listas vacías para almacenar calificaciones por cada aptitud
        self.historialCalificaciones = [ [] for _ in range(len(self.aptitudes)) ]

        #agregar a la meta-clase serializadora el objeto Actor en las listas actores y artistas
        Teatro.getInstancia().actores.append(self)
        Teatro.getInstancia().artistas.append(self)



    #cálculo que devuelve el contrato de un actor según las horas de trabajo y su calificación promedio
    def getPrecioContrato(self, horas: float) -> float:
        self.precioContrato = ((((super.calificacion**2) / 5) * Actor.TASA) / 8) * horas
        return self.precioContrato
    
    #halla la posición de la aptitud en la lista aptitudes, y en esa misma posición agrega la
    # calificación en calificacionesAptitudes
    def setCalificacionPorAptitud(self, aptitud: Aptitud, calificacion: float) -> None:
        index = self.aptitudes.index(aptitud)
        if index != -1:
            self.calificacionesAptitudes[index] = calificacion

    #halla la posición de la aptitud en la lista aptitudes y devuelve el indice correspondiente en
    # calificacionesAptitudes
    def getCalificacionPorAptitud(self, aptitud: Aptitud):
        index = self.aptitudes.index(aptitud)
        if index != -1:
            return self.calificacionesAptitudes[index]
        else:
            return -1
        

