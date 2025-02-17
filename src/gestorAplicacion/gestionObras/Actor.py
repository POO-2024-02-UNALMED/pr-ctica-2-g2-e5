from __future__ import annotations
from gestorAplicacion.gestionObras.Artista import Artista
from baseDatos.Teatro import Teatro
from gestorAplicacion.herramientas.Aptitud import Aptitud
from gestorAplicacion.gestionFinanciera.CuentaBancaria import CuentaBancaria
from functools import cmp_to_key

def format_cop(amount):
    return f"${amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

class Actor(Artista):
    TASA = 1_000_000
    __BAJA_CALIFICACION = 3

    def __init__(self, nombre: str, id: int, edad: int):
        super().__init__(nombre, id)

        self.__generos = []
        self.__notas = []
        self.__tiempoActuado = []
        self.__reevaluacion = False
        self.__precioContrato = None
        self.__sexo = None
        self.__edad = edad

        # segun las aptitudes que estén en el enum
        self.__aptitudes = [aptitud for aptitud in Aptitud]

        # inicializar calificaciones en 0
        self.__calificacionesAptitudes = [0.0] * len(self.__aptitudes)

        # lista de listas vacías para almacenar calificaciones por cada aptitud
        self.__historialCalificaciones = [[] for _ in range(len(self.__aptitudes))]

        # agregar a la meta-clase serializadora el objeto Actor en las listas actores y artistas
        Teatro.getInstancia().getActores().append(self)
        Teatro.getInstancia().getArtistas().append(self)

        self.__cuenta = CuentaBancaria(id, 9999999999999999999999999)

    #cálculo que devuelve el contrato de un actor según las horas de trabajo y su calificación promedio
    def getPrecioContrato(self, horas: float) -> float:
        self.__precioContrato = ((((super().getCalificacion()**2) / 5) * Actor.TASA) / 8) * horas
        return round(self.__precioContrato, 2)
    
    #halla la posición de la aptitud en la lista aptitudes, y en esa misma posición agrega la
    # calificación en calificacionesAptitudes
    def setCalificacionPorAptitud(self, aptitud: Aptitud, calificacion: float) -> None:
        index = self.__aptitudes.index(aptitud)
        if index != -1:
            self.__calificacionesAptitudes[index] = calificacion

    #halla la posición de la aptitud en la lista aptitudes y devuelve el indice correspondiente en
    # calificacionesAptitudes
    def getCalificacionPorAptitud(self, aptitud: Aptitud) -> float:
        index = self.__aptitudes.index(aptitud)
        if index != -1:
            return self.__calificacionesAptitudes[index]
        else:
            return -1

    def compare(self, a: float, b: float) -> int:
        if a < b: 
            return -1
        elif a > b: 
            return 1
        else: 
            return 0

    def obtenerAreasDeMejora(self) -> list:

        #Crear una lista de índices y ordenar según las calificaciones
        inidicesOrdenados = sorted([i for i in range(len(self.__aptitudes))], key = cmp_to_key(self.compare))

        #por cada indice, evaluar en aptitudes si su calificación es baja
        areasDeMejora = [self.__aptitudes[idx] for idx in inidicesOrdenados if self.getCalificacionPorAptitud(self.__aptitudes[idx]) <= Actor.__BAJA_CALIFICACION]

        return areasDeMejora
    
    def getHistorialCalificaciones(self, aptitud: Aptitud) -> list | None:
        #si existe el indice, devuelve la respecta lista de historial de calificacion 
        # para la aptitud pedida
        index = self.__aptitudes.index(aptitud)
        return self.__historialCalificaciones[index] if index != -1 else None 

    def registrarCalificacion(self, aptitud: Aptitud, calificacion: float) -> None:
        index = self.__aptitudes.index(aptitud)
        return self.__historialCalificaciones[index].append(calificacion)
    
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
        inicial = [0] * len(self.__aptitudes)
        return inicial == self.__calificacionesAptitudes
    
    def getGeneros(self):
        return self.__generos

    def setGeneros(self, value):
        self.__generos = value

    def getNotas(self):
        return self.__notas

    def setNotas(self, value):
        self.__notas = value

    def getTiempoActuado(self):
        return self.__tiempoActuado
    
    def setTiempoActuado(self, value):
        self.__tiempoActuado = value

    def isReevaluacion(self):
        return self.__reevaluacion

    def setReevaluacion(self, value):
        self.__reevaluacion = value

    def setPrecioContrato(self, value):
        self.__precioContrato = value

    def getAptitudes(self):
        return self.__aptitudes

    def setAptitudes(self, value):
        self.__aptitudes = value

    def getCalificacionesAptitudes(self):
        return self.__calificacionesAptitudes

    def setCalificacionesAptitudes(self, value):
        self.__calificacionesAptitudes = value

    def setHistorialCalificaciones(self, value):
        self.__historialCalificaciones = value

    def getCuenta(self):
        return self.__cuenta

    def setCuenta(self, value):
        self.__cuenta = value

    def getSexo(self):
        return self.__sexo
    
    def setSexo(self, value):
        self.__sexo = value

    def getEdad(self):
        return self.__edad
    
    def setEdad(self, value):
        self.__edad = value