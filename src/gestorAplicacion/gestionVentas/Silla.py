from gestorAplicacion.herramientas import Asiento;

class Silla:
    def __init__(self, tipo: Asiento, codigo: int):
        self.__tipo = tipo
        self.__codigo = codigo

    # Métodos getter y setter 

    # Tipo
    def getTipo(self) -> Asiento:
        return self.__tipo

    def setTipo(self, tipo: Asiento):
        self.__tipo = tipo

    # Código
    def getCodigo(self) -> int:
        return self.__codigo

    def setCodigo(self, codigo: int):
        self.__codigo = codigo