from gestorAplicacion.herramientas.Persona import Persona
from abc import abstractmethod
from datetime import datetime

class PersonaConHorario(Persona):

    horario: list
    nombre: str

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