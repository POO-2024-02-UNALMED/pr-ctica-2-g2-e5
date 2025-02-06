from __future__ import annotations
from abc import ABC
from src.gestorAplicacion.gestionFinanciera.CuentaBancaria import CuentaBancaria
from src.gestorAplicacion.gestionClases.Clase import Clase
from datetime import datetime
from baseDatos import Teatro
from random import random


class Artista(ABC):

    #constructor que se puede llamar solo con nombre e id
    def __init__(self, nombre: str, id: int, calificacion: float = 0, promedio: float = 0, clase: Clase = None):
        self.nombre = nombre
        self.id = id
        self.calificacion = calificacion
        self.promedio = promedio
        self.cuenta = CuentaBancaria()
        self.clase = clase

        self.horario = []
        self.calificaciones = []
        self.calificacionesPublico = []

        Teatro.getInstancia().artistas.add(self)

    #promedio de la lista de calificaciones
    def calcularCalificacion(self) -> None:
        self.calificacion = sum(self.calificaciones) / len(self.calificaciones)           

    #revisa en cada intervalo de horarios guardados si el nuevo horario se solapa
    def isDisponible(self, inicio: datetime, fin: datetime) -> bool:
        for evento in self.horario:
            if ((inicio < evento[0]) and (fin > evento[1])):
                return False
        return True
    
    @classmethod
    def buscarArtistaPorId(id: int) -> Artista | None:
        for artista in Teatro.getInstancia().artistas:
            if (artista.id == id):
                return artista
        return None
    
    @classmethod
    def inicializarCalificacionesPublico(artista: Artista) -> None:
        artista.calificacionesPublico += [ round(random() * 5, 2) for i in range(5)]


