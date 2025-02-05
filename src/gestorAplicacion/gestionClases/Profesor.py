import random
from gestorAplicacion.gestionFinanciera import Empleado
from gestorAplicacion.herramientas import Aptitud

class Profesor(Empleado):
    def __init__(self, nombre: str, id: int):
        super().__init__(nombre, id, "Profesor")  # Llamamos al constructor de la clase base
        
        self.especializaciones = []
        valores = list(Aptitud)  
        while len(self.especializaciones) < 2:
            seleccionada = random.choice(valores)
            if seleccionada not in self.especializaciones:
                self.especializaciones.append(seleccionada)

    def agregar_especializacion(self, aptitud: Aptitud):   #Añade una especialización si no está repetida
        if aptitud not in self.especializaciones:
            self.especializaciones.append(aptitud)

    def tiene_especializacion(self, aptitud: Aptitud):   #Verifica si el profesor tiene una especialización específica.
        return aptitud in self.especializaciones

    def agregar_puntos(self, puntos: int):   #Agrega puntos positivos al profesor
        self.puntos_positivos += puntos