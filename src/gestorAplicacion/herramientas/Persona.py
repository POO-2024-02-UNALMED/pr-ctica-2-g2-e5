from __future__ import annotations
from abc import ABC, abstractmethod

class Persona(ABC): 

    id: int

    #método estático-abstracto
    # estático para ser llamado desde la sublcase, 
    # abstracto para definir la lista donde se buscará la identificación
    @staticmethod
    @abstractmethod
    def buscarPorId(cls, id: int) -> Persona | bool:
        """Busca en la lista de instancia Teatro respectiva, si el número de identificación existe"""
        pass
    
    #métodos abstractos
    @abstractmethod
    def getId(self) -> int:
        pass

    @abstractmethod
    def setId(self, value: int) -> None:
        pass