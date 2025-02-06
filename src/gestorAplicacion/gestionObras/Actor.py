from gestorAplicacion.gestionObras.Artista import Artista
from baseDatos.Teatro import Teatro
from gestorAplicacion.herramientas.Aptitud import Aptitud
from gestionFinanciera.CuentaBancaria import CuentaBancaria
from functools import cmp_to_key

def format_cop(amount):
    return f"${amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

class Actor(Artista):
    TASA = 1_000_000
    BAJA_CALIFICACION = 3

    def __init__(self, nombre: str, id: int):
        super.__init__(nombre, id)

        self.generos = []
        self.notas = []
        self.tiempoActuado = []
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

        self.cuenta = CuentaBancaria(id, 9999999999999999999999999)


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
    def getCalificacionPorAptitud(self, aptitud: Aptitud) -> int:
        index = self.aptitudes.index(aptitud)
        if index != -1:
            return self.calificacionesAptitudes[index]
        else:
            return -1

    def compare(a: float, b: float) -> int:
        if a < b: return -1
        elif a > b: return 1
        else: return 0

    def obtenerAreasDeMejora(self) -> list:

        #Crear una lista de índices y ordenar según las calificaciones
        inidicesOrdenados = sorted([i for i in range(len(self.aptitudes))], key = cmp_to_key(self.compare))

        #por cada indice, evaluar en aptitudes si su calificación es baja
        areasDeMejora = [self.aptitudes[idx] for idx in inidicesOrdenados if self.getCalificacionPorAptitud(self.aptitudes[idx]) <= Actor.BAJA_CALIFICACION]

        return areasDeMejora
    
    def getHistorialCalificaciones(self, aptitud: Aptitud) -> list | None:
        #si existe el indice, devuelve la respecta lista de historial de calificacion 
        # para la aptitud pedida
        index = self.aptitudes.index(aptitud)
        return self.historialCalificaciones[index] if index != -1 else None 

    def registrarCalificacion(self, aptitud: Aptitud, calificacion: float) -> None:
        index = self.aptitudes.index(aptitud)
        return self.historialCalificaciones[index].append(calificacion)
    
    def huboMejora(self, aptitud: Aptitud) -> bool:

        calificaciones = self.getHistorialCalificaciones(aptitud)
        n = len(calificaciones)

        if (calificaciones is None) or (n < 2): return False
        return calificaciones[n - 1] > calificaciones[n - 2]
    
    def noHaMejoradoEnCuatroIntentos(self, aptitud: Aptitud) -> bool:

        calificaciones = self.getHistorialCalificaciones(aptitud)
        n = len(calificaciones)

        if (calificaciones is None) or (n < 4): return False

        return (calificaciones[n - 1] <= calificaciones[n - 2]) and (calificaciones[n - 2] <= calificaciones[n - 3]) and (calificaciones[n - 3] <= calificaciones[n - 4])
    
    def sigueIgual(self) -> bool:
        inicial = [0] * len(self.aptitudes)
        return inicial == self.calificacionesAptitudes