from __future__ import annotations
from gestorAplicacion.gestionFinanciera.Tesoreria import Tesoreria

class Teatro:

    __instancia = None

    def __init__(self):

        self.tesoreria = Tesoreria(100, 10)

        # empleados
        self.__empleadosPorRendimiento = []
        self.__tipoSeguridad = []
        self.__tipoAseador = []
        self.__tipoProfesor = []

        # artistas
        self.__artistas = []
        self.__actores = []
        self.__directors = []

        # obras
        self.__obras = []
        self.__estadoCriticoS = []

        # clientes
        self.__clientes = []

        # funciones
        self.__funcionesCreadas = []
        self.__asistentes = []

        # salas
        self.__salas = []

        # tiquetes
        self.__tiquetes = []

    @classmethod
    def getInstancia(cls):
        return cls.__instancia
    
    @classmethod
    def setInstancia(cls, teatro: Teatro) -> None:
        cls.__instancia = teatro

    def getEmpleadosPorRendimiento(self):
        return self.__empleadosPorRendimiento

    def setEmpleadosPorRendimiento(self, value):
        self.__empleadosPorRendimiento = value

    def getTipoSeguridad(self):
        return self.__tipoSeguridad

    def setTipoSeguridad(self, value):
        self.__tipoSeguridad = value

    def getTipoAseador(self):
        return self.__tipoAseador

    def setTipoAseador(self, value):
        self.__tipoAseador = value

    def getTipoProfesor(self):
        return self.__tipoProfesor

    def setTipoProfesor(self, value):
        self.__tipoProfesor = value

    def getArtistas(self):
        return self.__artistas

    def setArtistas(self, value):
        self.__artistas = value

    def getActores(self):
        return self.__actores

    def setActores(self, value):
        self.__actores = value

    def getDirectors(self):
        return self.__directors

    def setDirectors(self, value):
        self.__directors = value

    def getObras(self):
        return self.__obras

    def setObras(self, value):
        self.__obras = value

    def getEstadoCriticoS(self):
        return self.__estadoCriticoS

    def setEstadoCriticoS(self, value):
        self.__estadoCriticoS = value

    def getClientes(self):
        return self.__clientes
    
    def setClientes(self, value):
        self.__clientes = value

    def getFuncionesCreadas(self):
        return self.__funcionesCreadas

    def setFuncionesCreadas(self, value):
        self.__funcionesCreadas = value

    def getAsistentes(self):
        return self.__asistentes

    def setAsistentes(self, value):
        self.__asistentes = value

    def getSalas(self):
        return self.__salas

    def setSalas(self, value):
        self.__salas = value

    def getTiquetes(self):
        return self.__tiquetes

    def setTiquetes(self, value):
        self.__tiquetes = value

    @classmethod
    def createInstancia(cls):
        if cls.__instancia is None:
            cls.__instancia = Teatro()