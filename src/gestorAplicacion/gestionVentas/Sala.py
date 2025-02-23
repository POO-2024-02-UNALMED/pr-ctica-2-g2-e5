

import datetime

from baseDatos.Teatro import Teatro




class Sala:

    def __init__(self, numero_sala: int, metros_cuadrados: float = 50.0, aseado: bool = True,
            ocupado: bool = False, capacidad: int = 100):
        self.__sillas = self.create_sillas(capacidad)
        self.__numero_sala = numero_sala
        self.__metros_cuadrados = metros_cuadrados
        self.__aseado = aseado
        self.__ocupado = ocupado
        self.__horario = []
        self.__capacidad = capacidad
        Teatro.getInstancia().getSalas().append(self)
        


    # Getters
    def get_sillas(self):
        return self.__sillas

    def set_sillas(self, sillas):
        self.__sillas = sillas

    def get_horario(self):
        return self.__horario

    def set_horario(self, horario):
        self.__horario = horario

    def get_numero_sala(self):
        return self.__numero_sala

    def get_metros_cuadrados(self):
        return self.__metros_cuadrados

    def get_aseado(self):
        return self.__aseado

    def get_ocupado(self):
        return self.__ocupado

    def get_capacidad(self):
        return self.__capacidad

    # Setters 
    def set_numero_sala(self, value):
        self.__numero_sala = value

    def set_metros_cuadrados(self, value):
        self.__metros_cuadrados = value

    def set_aseado(self, value):
        self.__aseado = value

    def set_ocupado(self, value):
        self.__ocupado = value

    def set_capacidad(self, value):
        self.__capacidad = value

    def is_disponible(self, inicio, fin) -> bool:
        for evento in self.get_horario():
            if inicio <= evento[1] or fin >= evento[0]:  
                return False  # Horario ocupado
        return True
    
    def calc_capacidad(self) -> int:
        """Calcula la cantidad de sillas disponibles."""
        return len(self.sillas)

    def anadir_horario(self, horario):
        """Añade un nuevo horario a la lista de horarios."""
        self.get_horario().append(horario)
    
    def create_sillas(self,capacidad: int) -> list:
        from gestorAplicacion.gestionVentas.Silla import Silla
        from gestorAplicacion.herramientas.Asiento import Asiento
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
        return str(self.get_numero_sala())