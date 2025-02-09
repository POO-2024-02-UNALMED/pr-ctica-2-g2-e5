from __future__ import annotations
from abc import ABC
from src.gestorAplicacion.gestionFinanciera.CuentaBancaria import CuentaBancaria
from src.gestorAplicacion.gestionClases.Clase import Clase
from datetime import datetime
from baseDatos import Teatro
from random import random
from typing import Optional


class Artista(ABC):

    #constructor que se puede llamar solo con nombre e id
    def __init__(self, nombre: str, id: int, calificacion: float = 0, promedio: float = 0, clase: Clase = None):
        self.__nombre = nombre
        self.__id = id
        self.__calificacion = calificacion
        self.__promedio = promedio
        self.__cuenta = CuentaBancaria()
        self.__clase = clase

        self.__horario = []
        self.__calificaciones = []
        self.__calificacionesPublico = []

        Teatro.getInstancia().getArtistas().add(self)

    #promedio de la lista de calificaciones
    def calcularCalificacion(self) -> None:
        self.__calificacion = sum(self.__calificaciones) / len(self.__calificaciones)           

    #revisa en cada intervalo de horarios guardados si el nuevo horario se solapa
    def isDisponible(self, inicio: datetime, fin: datetime) -> bool:
        for evento in self.__horario:
            if ((inicio < evento[0]) and (fin > evento[1])):
                return False
        return True
    
    @classmethod
    def buscarArtistaPorId(id: int) -> Optional[Artista]:
        for artista in Teatro.getInstancia().getArtistas():
            if (artista.getId() == id):
                return artista
        return None
    
    @classmethod
    def inicializarCalificacionesPublico(artista: Artista) -> None:
        artista.__calificacionesPublico += [ round(random() * 5, 2) for i in range(5)]
 
    def getNombre(self):
        return self.__nombre

    def setNombre(self, value):
        self.__nombre = value

    def getId(self):
        return self.__id

    def setId(self, value):
        self.__id = value

    def getCalificacion(self):
        return self.__calificacion

    def setCalificacion(self, value):
        self.__calificacion = value

    def getPromedio(self):
        return self.__promedio

    def setPromedio(self, value):
        self.__promedio = value

    def getCuenta(self):
        return self.__cuenta

    def setCuenta(self, value):
        self.__cuenta = value

    def getClase(self):
        return self.__clase

    def setClase(self, value):
        self.__clase = value

    def getHorario(self):
        return self.__horario

    def setHorario(self, value):
        self.__horario = value

    def getCalificaciones(self):
        return self.__calificaciones

    def setCalificaciones(self, value):
        self.__calificaciones = value

    def getCalificacionesPublico(self):
        return self.__calificacionesPublico

    def setCalificacionesPublico(self, value):
        self.__calificacionesPublico = value