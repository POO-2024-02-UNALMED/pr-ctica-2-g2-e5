from datetime import datetime
from typing import List, Tuple

from gestorAplicacion.gestionClases import Profesor
from gestorAplicacion.gestionObras import Artista
from gestorAplicacion.gestionVentas import Sala

class Clase:
    def __init__(self, profesor: Profesor, alumno: Artista, aprobada: bool, costo_matricula: float, 
                 materia_nombre: str, nivel: int, sala: Sala):
        self.profesor = profesor              
        self.alumno = alumno                  
        self.horario = []                     
        self.aprobada = aprobada              
        self.costo_matricula = costo_matricula  
        self.materia_nombre = materia_nombre  
        self.nivel = nivel                    
        self.sala = sala                    

    def agregar_horario(self, inicio: datetime, fin: datetime):
        self.horario.append((inicio, fin))
    
    def verificar_disponibilidad(self, inicio: datetime, fin: datetime):
        for intervalo in self.horario:
            if inicio < intervalo[1] and fin > intervalo[0]:
                return False  # Hay un choque de horarios
        return True  # No hay conflictos