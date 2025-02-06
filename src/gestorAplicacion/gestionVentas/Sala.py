

class Sala:
    salas = []  # Lista estática de salas

    def __init__(self, numero_sala: int = 1, metros_cuadrados: float = 50.0, aseado: bool = True,
                 ocupado: bool = False, capacidad: int = 100):
        self.sillas = []
        self.numero_sala = numero_sala
        self.metros_cuadrados = metros_cuadrados
        self.aseado = aseado
        self.ocupado = ocupado
        self.horario = []
        self.capacidad = capacidad
        Sala.salas.append(self)  # Agregar instancia a la lista de salas

