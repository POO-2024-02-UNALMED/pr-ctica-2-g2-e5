from __future__ import annotations
from datetime import datetime
from abc import ABC, abstractmethod

class Persona(ABC): 

    id: int
    horario: list
    nombre: str

    #método estático-abstracto
    # estático para ser llamado desde la sublcase, 
    # abstracto para definir la lista donde se buscará la identificación
    @staticmethod
    @abstractmethod
    def buscarPorId(cls, id: int) -> Persona | None:
        """Busca en la lista de instancia Teatro respectiva, si el número de identificación existe"""
        pass
    
    #método por default
    def isDisponible(self, inicio: datetime, fin: datetime) -> bool:
        """Revisa en cada intervalo de horarios guardados si el nuevo horario se solapa"""
        for evento in self.getHorario():
            if ((inicio < evento[1]) and (fin > evento[0])):
                return False
        return True
    
    #métodos abstractos
    @abstractmethod
    def getNombre(self) -> str:
        pass

    @abstractmethod
    def setNombre(self, value: str) -> None:
        pass

    @abstractmethod
    def getHorario(self) -> list:
        pass

    @abstractmethod
    def setHorario(self, value: list) -> None:
        pass