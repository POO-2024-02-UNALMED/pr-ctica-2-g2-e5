from gestionFinanciera.CuentaBancaria import CuentaBancaria
from gestorAplicacion.gestionObras.Actor import Actor
from random import random
from gestorAplicacion.herramientas.Aptitud import Aptitud
class Empleado: 
    SALARIOSEGURIDAD = 6500
    SALARIOASEADOR = 5500
    SALARIOPROFESOR = 5500

    def __init__(self, nombre, ID, Ocupacion):
        self.nombre = nombre
        self.id = ID
        self.ocupacion = Ocupacion
        self.cuenta = CuentaBancaria(ID, 0)
        self.metaSemanal = 6
        self.puntosPositivos = 0
        self.disponible = True
        self.deuda = 0
        self.horario = []
        self.trabajoRealizado = 0
        self.trabajoCorrecto = []
        self.trabajos = []
    
    #Calcular Sueldo
    def calcularSueldo(self):
        if self.__ocupacion == "Seguridad":
            sueldo = self.trabajoRealizado * self.SALARIOSEGURIDAD
            return sueldo
        elif self.__ocupacion == "Aseador":
            sueldo = self.trabajoRealizado * self.SALARIOASEADOR
            return sueldo
        else: #Profesor
            sueldo = self.trabajoRealizado * self.SALARIOPROFESOR
            return sueldo
    
    def verificacionMeta(self):
        if self.__trabajoRealizado >= self.metaSemanal:
            return True
        else:
            return False

    #Casting
    def casting(self, artista, profesores):
        if not isinstance(artista, Actor):
            return False
        if not profesores:
            return False    
        aptitud = Aptitud.values
        for i in range(0, 5):
            artista.setCalificacionPorAptitud(aptitud[i],round(random()*50 / 10.0, 1))
        return True

    