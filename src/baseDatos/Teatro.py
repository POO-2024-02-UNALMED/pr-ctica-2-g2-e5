import gestorAplicacion.gestionFinanciera.Tesoreria

class Teatro:

    _instancia = None

    def __init__(self):

        self.tesoreria = Tesoreria()
        
        #empleados
        self.empleadosPorRendimiento = []
        self.tipoSeguridad = []
        self.tipoAseador = []
        self.tipoProfesor = []
        
        #artistas
        self.artistas = []
        self.actores = []
        self.directors = []

        #obras
        self.obras = []
        self.estadoCriticoS = []

        #clientes
        self.clientes = []

        #funciones
        self.funcionesCreadas = []
        self.asistentes = []

        #salas
        self.salas = []

        #tiquetes
        self.tiquetes = []

    def getInstancia(self):
        return self._instancia


