from datetime import datetime
from typing import List, Tuple

from gestorAplicacion.gestionClases import Profesor
from gestorAplicacion.gestionObras import Artista
from gestorAplicacion.gestionVentas import Sala

class Clase:
    def __init__(self, profesor: Profesor, alumno: Artista, aprobada: bool, costo_matricula: float, 
                 materia_nombre: str, nivel: int, sala: Sala):
        self.__profesor = profesor          
        self.__alumno = alumno               
        self.__horario: List[Tuple[datetime, datetime]] = [] 
        self.__aprobada = aprobada             
        self.__costoMatricula = costo_matricula 
        self.__materiaNombre = materia_nombre  
        self.__nivel = nivel                    
        self.__sala = sala    

    # Métodos getter y setter

    # Profesor
    def getProfesor(self):
        return self.__profesor

    def setProfesor(self, profesor):
        self.__profesor = profesor

    # Alumno
    def getAlumno(self):
        return self.__alumno

    def setAlumno(self, alumno):
        self.__alumno = alumno

    # Horario
    def getHorario(self) -> List[Tuple[datetime, datetime]]:
        return self.__horario

    def setHorario(self, horario: List[Tuple[datetime, datetime]]):
        self.__horario = horario

    # Aprobada
    def getAprobada(self) -> bool:
        return self.__aprobada

    def setAprobada(self, aprobada: bool):
        self.__aprobada = aprobada

    # CostoMatricula
    def getCostoMatricula(self) -> float:
        return self.__costoMatricula

    def setCostoMatricula(self, costo: float):
        self.__costoMatricula = costo

    # MateriaNombre
    def getMateriaNombre(self) -> str:
        return self.__materiaNombre

    def setMateriaNombre(self, nombre: str):
        self.__materiaNombre = nombre

    # Nivel
    def getNivel(self) -> int:
        return self.__nivel

    def setNivel(self, nivel: int):
        self.__nivel = nivel

    # Sala
    def getSala(self):
        return self.__sala

    def setSala(self, sala):
        self.__sala = sala

    # Métodos funcionales

    def agregarHorario(self, inicio: datetime, fin: datetime):
        """Agrega un intervalo de horario (inicio, fin) a la lista de horarios."""
        self.__horario.append((inicio, fin))
    
    def verificarDisponibilidad(self, inicio: datetime, fin: datetime) -> bool:
        """
        Verifica que el intervalo [inicio, fin] no choque con ninguno de los intervalos existentes.
        Retorna True si no hay conflictos y False en caso contrario.
        """
        for intervalo in self.__horario:
            if inicio < intervalo[1] and fin > intervalo[0]:
                return False  # Existe un choque de horarios
        return True  # No hay conflictos