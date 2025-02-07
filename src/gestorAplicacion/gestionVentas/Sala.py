

import datetime


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

    def is_disponible(self, inicio, fin) -> bool:
        for evento in self.horario:
            if inicio < evento[1] and fin > evento[0]:  
                return False  # Horario ocupado
        return True
    
    def calc_capacidad(self) -> int:
        """Calcula la cantidad de sillas disponibles."""
        return len(self.sillas)

    def anadir_horario(self, horario):
        """Añade un nuevo horario a la lista de horarios."""
        self.horario.append(horario)
    
    def create_sillas(capacidad: int) -> List[Silla]:
        """Crea una lista de sillas distribuidas según la capacidad dada."""
        u = capacidad // 16  # División entera
        f, s, o, p = 0, 10, 100, 1000
        sillas = []

        # Agregar sillas GOLD
        for _ in range(u * 2):
            sillas.append(Silla(Asiento.GOLD, f))
            f += 1

        # Agregar sillas PREMIUM
        for _ in range(u * 2):
            sillas.append(Silla(Asiento.PREMIUM, s))
            s += 1

        # Agregar sillas COMFORT
        for _ in range(u * 4):
            sillas.append(Silla(Asiento.COMFORT, o))
            o += 1

        # Agregar sillas BASICO
        for _ in range(u * 8):
            sillas.append(Silla(Asiento.BASICO, p))
            p += 1

        # Completar con sillas BASICO si falta capacidad
        while len(sillas) < capacidad:
            sillas.append(Silla(Asiento.BASICO, p))
            p += 1

        return sillas
    
    def __str__(self):
        return str(self.numero_sala)