from gestionFinanciera.CuentaBancaria import CuentaBancaria

class Empleado: 
    SALARIOSEGURIDAD = 6500
    SALARIOASEADOR = 5500
    SALARIOPROFESOR = 5500

    def __init__(self, nombre, ID, Ocupacion):
        self._nombre = nombre
        self.__id = ID
        self.__ocupacion = Ocupacion
        self.__cuenta = CuentaBancaria(ID, 0)
        self.__metaSemanal = 6
        self.__puntosPositivos = 0
        self.__disponible = True
        self.__deuda = 0
        self.__horario = []
        self.__trabajoRealizado = 0
        self.__trabajoCorrecto = []
        self.__trabajos = []
    
    #Calcular Sueldo
    def calcularSueldo(self):
        if self.__ocupacion == "Seguridad":
            sueldo = self.__trabajoRealizado * self.SALARIOSEGURIDAD
            return sueldo
        elif self.__ocupacion == "Aseador":
            sueldo = self.__trabajoRealizado * self.SALARIOASEADOR
            return sueldo
        else: #Profesor
            sueldo = self.__trabajoRealizado * self.SALARIOPROFESOR
            return sueldo
    
    def verificacionMeta(self):
        if self.__trabajoRealizado >= self.__metaSemanal:
            return True
        else:
            return False
    
    #Getters and Setters
    #Nombre
    def getNombre(self):
        return self._nombre
    
    def setNombre(self, nombre):
        self._nombre = nombre
    
    #ID
    def getId(self): 
        return self.__id
    
    def setId(self, ID):
        self.__id = ID
    
    #Ocupacion
    def getOcupacion(self):
        return self.__Ocupacion
    
    def setOcupacion(self, Ocupacion):
        self.__Ocupacion = Ocupacion

    #Trabajos
    def getTrabajoRealizado(self):
        return self.__trabajoRealizado
    
    def setTrabajoRealizado(self, trabajoRealizado):
        self.__trabajoRealizado = trabajoRealizado
    
    def getTrabajoCorrecto(self):
        return self.__trabajoCorrecto
    
    def setTrabajoCorrecto(self, trabajoCorrecto):
        self.__trabajoCorrecto = trabajoCorrecto
    
    def getTrabajos(self):
        return self.__trabajos
    
    def setTrabajos(self, trabajos):
        self.__trabajos = trabajos
    
    #Meta
    def getMetaSemanal(self):
        return self.__metaSemanal
    
    def setMetaSemanal(self, metaSemanal): 
        self.__metaSemanal = metaSemanal
    
    #Puntos Positivos
    def getPuntosPositivos(self):
        return self.__puntosPositivos
    
    def setPuntosPositivos(self, puntosPositivos):
        self.__puntosPositivos = puntosPositivos
    
    #Disponible
    def isDisponible(self):
        return self.__disponible
    
    def setDisponible(self, disponible):
        self.__disponible = disponible
    
    #Deuda
    def getDeuda(self):
        return self.__deuda
    
    def setDeuda(self, deuda):
        self.__deuda = deuda
    
    #Cuenta
    def getCuenta(self):
        return self.__cuenta
    
    def setCuenta(self, cuenta):
        self.__cuenta = cuenta

    #Horario
    def getHorario(self):
        return self.__horario
    
    def setHorario(self, horario):
        self.__horario = horario
    
    #Salario
    def getSalarioSeguridad(self):
        return self.SALARIOSEGURIDAD
    
    def getSalarioAseador(self):
        return self.SALARIOASEADOR
    
    def getSalarioProfesor(self):
        return self.SALARIOPROFESOR
    
    