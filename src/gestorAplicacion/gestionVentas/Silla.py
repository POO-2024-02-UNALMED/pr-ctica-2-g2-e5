from gestorAplicacion.herramientas import Asiento;

class Silla:
    def __init__(self, tipo: Asiento, codigo: int):
        self.tipo = tipo
        self.codigo = codigo