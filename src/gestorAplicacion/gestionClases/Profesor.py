import random
from gestorAplicacion.gestionFinanciera import Empleado
from gestorAplicacion.herramientas import Aptitud

class Profesor(Empleado):
    def __init__(self, nombre: str, id: int):
        super().__init__(nombre, id, "Profesor")  # Llamamos al constructor de la clase base
        
        self.__especializaciones = []
        valores = list(Aptitud)  
        #Se asignan dos aptitudes aleatorias sin repetir
        while len(self.especializaciones) < 2:
            seleccionada = random.choice(valores)
            if seleccionada not in self.especializaciones:
                self.especializaciones.append(seleccionada)

    # Métodos getter y setter para especializaciones

    def getEspecializaciones(self):
        return self.__especializaciones

    def setEspecializaciones(self, especializaciones):
        self.__especializaciones = especializaciones

    # Métodos funcionales

    def agregar_especializacion(self, aptitud: Aptitud):   #Añade una especialización si no está repetida
        if aptitud not in self.especializaciones:
            self.especializaciones.append(aptitud)

    def tiene_especializacion(self, aptitud: Aptitud):   #Verifica si el profesor tiene una especialización específica.
        return aptitud in self.especializaciones

    def agregar_puntos(self, puntos: int):   #Agrega puntos positivos al profesor
        self.puntos_positivos += puntos

    # Opcional: Getters y setters para el atributo nombre, si se requiere
    
    def getNombre(self) -> str:
        return self._nombre  # Se asume que _nombre es definido en la clase base Empleado

    def setNombre(self, nombre: str):
        self._nombre = nombre