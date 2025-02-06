

class Funcion:
    funciones_creadas = []  # Lista estática de funciones creadas
    funciones_a_la_venta = []  # Lista estática de funciones a la venta

    def __init__(self, obra = None, tiquetes_vendidos: int = 0, sala = None, calificador: bool = False,
                 audiencia_esperada: int = 0, trabajador: bool = False, precio: float = 0.0):
        self.obra = obra
        self.tiquetes_vendidos = tiquetes_vendidos
        self.horario = []
        self.sillas  = []
        self.sala = sala
        self.calificador = calificador
        self.audiencia_esperada = audiencia_esperada
        self.trabajador = trabajador
        self.asistentes = []
        self.precio = precio
        Funcion.funciones_creadas.append(self)
    