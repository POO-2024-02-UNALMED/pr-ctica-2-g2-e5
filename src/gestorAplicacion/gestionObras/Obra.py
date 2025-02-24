import datetime
import random
import time

from baseDatos.Teatro import Teatro
from gestorAplicacion.herramientas import Genero

class Obra:
    estadoCriticoS = []
    obras = []
    def __init__(self, audienciaEsperada = 0, nombre = "", calificacion = 0, reparto = [], papeles = [], director = None, costoProducción = 0, funcionesSemana = [], genero = None, tiquetesTotales = 0, estadoCriticoA = False, calificaciones = [], franjaHoraria = [],
                duracion = None, funcionEstelar = None, funciones = [], funcionesRecomendadas = 0, promedioArt = 0, repartoDisponible = False, asistencia = 0, precio = 0):
        self.__audienciaEsperada = audienciaEsperada
        self.__nombre = nombre
        self.__calificacion = calificacion
        self.__reparto = reparto
        self.__papeles = papeles
        self.__director = director
        self.__costoProduccion = costoProducción
        self.__funcionesSemana = funcionesSemana
        self.__genero = genero
        self.__tiquetesTotales = tiquetesTotales
        self.__estadoCriticoA = estadoCriticoA
        self.__calificaciones = calificaciones
        self.__franjaHoraria = franjaHoraria
        self.__duracion = duracion
        self.__funcionEstelar = funcionEstelar
        self.__funciones = funciones
        self.__funcionesRecomendadas = funcionesRecomendadas
        self.__promedioArt = promedioArt
        self.__repartoDisponible = repartoDisponible
        self.__asistencia = asistencia
        self.__precio = precio
        self.calcularCalificacion(self.getCalificaciones())
        self.calcAudienciaEsperada(self.getCalificacion())
        self.checkEstadoCritico()
        Teatro.getInstancia().getObras().append(self)
        Obra.obras.append(self)
        
    def getAudienciaEsperada(self):
        return self.__audienciaEsperada
    
    def setAudienciaEsperada(self, value):
        self.audienciaEsperada = value  
    
    def getNombre(self):    
        return self.__nombre
    
    def setNombre(self, value):
        self.nombre = value
    
    def getCalificacion(self):
        return self.__calificacion
    
    def setCalificacion(self, value):
        self.calificacion = value
        
    def getReparto(self):
        return self.__reparto
    
    def setReparto(self, value):
        self.reparto = value
    
    def getPapeles(self):
        return self.__papeles
    
    def setPapeles(self, value):
        self.papeles = value
    
    def getDirector(self):
        return self.__director
    
    def setDirector(self, value):
        self.director = value
    
    def getCostoProduccion(self):
        return self.__costoProduccion
    
    def setCostoProduccion(self, value):
        self.costoProduccion = value
        
    def getFuncionesSemana(self):
        return self.__funcionesSemana
    
    def setFuncionesSemana(self, value):
        self.funcionesSemana = value
        
    def getGenero(self):
        return self.__genero
    
    def setGenero(self, value):
        self.genero = value
        
    def getTiquetesTotales(self):
        return self.__tiquetesTotales
    
    def setTiquetesTotales(self, value):
        self.tiquetesTotales = value
        
    def getEstadoCriticoA(self):
        return self.__estadoCriticoA
    
    def setEstadoCriticoA(self, value):
        self.estadoCriticoA = value
        
    def getCalificaciones(self):
        return self.__calificaciones
    
    def setCalificaciones(self, value):
        self.calificaciones = value
        
    def getFranjaHoraria(self):
        return self.__franjaHoraria
    
    def setFranjaHoraria(self, value):
        self.__franjaHoraria = value
        
    def getDuracion(self):
        return self.__duracion
    
    def setDuracion(self, value):
        self.duracion = value
        
    def getFuncionEstelar(self):
        return self.__funcionEstelar
    
    def setFuncionEstelar(self, value):
        self.__funcionEstelar = value
        
    def getFunciones(self):
        return self.__funciones
    
    def setFunciones(self, value):
        self.funciones = value
        
    def getFuncionesRecomendadas(self):
        return self.__funcionesRecomendadas
    
    def setFuncionesRecomendadas(self, value):  
        self.funcionesRecomendadas = value
        
    def getPromedioArt(self):
        return self.__promedioArt
    
    def setPromedioArt(self, value):
        self.promedioArt = value
        
    def getRepartoDisponible(self):
        return self.__repartoDisponible
    
    def setRepartoDisponible(self, value):
        self.repartoDisponible = value
        
    def getAsistencia(self):
        return self.__asistencia
    
    def setAsistencia(self, value):
        self.asistencia = value
        
    def getPrecio(self):
        return self.__precio
    
    def setPrecio(self, value):
        self.__precio = value

    def funcionesRecomendadas(self, promedioArt):
        if promedioArt < 2:
            return 3
        elif promedioArt < 3:
            return 5
        elif promedioArt < 4:
            return 7
        else:
            return 10

    def calcAudienciaEsperada(self, calificacion):
        u = calificacion * 12
        self.setAudienciaEsperada(u)
        
    def calcularCalificacion(self, calificaciones):
        u = 0
        t = 1
        for i in calificaciones:
            u = u + i
            t = t+1
        v = u / t
        self.setCalificacion(v)

    def franjaHoraria(self, genero):
        from gestorAplicacion.gestionVentas import Funcion
        from baseDatos import Teatro
        import datetime

        # Inicializa la franja horaria con valores extremos
        franja = [datetime.time(hour=0, minute=0), datetime.time(hour=23, minute=59)]
        a = Funcion.Funcion(horario = [datetime.datetime(year=2024,month=1,day=2,hour=0,minute=0), datetime.datetime(year=2024,month=1,day=2,hour=0,minute=0)])
        franja = [datetime.time(hour=00,minute=00),datetime.time(hour=23,minute=59)]
        obrasGenero = []

        # Filtra las obras por género
        for obra in Teatro.Teatro.getInstancia().getObras():
            if obra.getGenero() == genero:
                obrasGenero.append(obra)

        # Revisa las funciones estelares de las obras filtradas
        for obra in obrasGenero:
            funcion_estelar = obra.getFuncionEstelar()
            if funcion_estelar is not None:
                fstar = funcion_estelar.extraerHora()  # Asegúrate de que esto devuelva una lista de datetime
                if len(fstar) >= 2:
                    # Extrae las horas de inicio y fin
                    hora_inicio = fstar[0]  # Asegúrate de que esto sea un objeto datetime
                    hora_fin = fstar[1]    # Asegúrate de que esto sea un objeto datetime

                    # Actualiza la franja horaria
                    if hora_inicio > franja[0]:
                        franja[0] = hora_inicio
                    if hora_fin < franja[1]:
                        franja[1] = hora_fin

        # Establece la franja horaria
        self.setFranjaHoraria(franja)

    def  calcFuncionEstelar(self,funciones):
        from gestionVentas import Funcion
        u = Funcion()
        v = Funcion()
        u.setTiquetesVendidos(0)
        s = u.getTiquetesVendidos()
        for funcion in funciones:
            d = funcion.getTiquetesVendidos
            if s < d:
                s = d
                v = funcion
        self.setFuncionEstelar(v)

    def checkEstadoCritico(self):
        return self.getCalificacion() < 1

    def calificacionVacia(self):
        return len(self.getCalificaciones()) != 0

    def promedioCalificacion(self):
        suma=0
        contador = 0
        if self.calificacionVacia() == False :
            return 0
        for cal in  self.getCalificaciones():
            suma = suma + cal
            contador = contador + 1
        return (suma / contador)
        
    def recurrencia(self):
        self.setAsistencia(self.getAsistencia() + 1)
    
    def precioFuncion(self):
            
            prom = random.randint(1,10)

            
            precioBase = 10000
            ad = 0
            if prom > 8:
                precioBase = precioBase + prom * 800 + ad

            elif prom > 5:
                precioBase = precioBase + prom * 400 + ad
            
            elif prom > 3:
                precioBase = precioBase + prom * 200 + ad

            else:
                precioBase = precioBase + prom * 100 + ad
            
            return precioBase
            

    def imprimirObra(self):
        return str.format(
            "%30s %20s %20s %20s",
            self.getNombre(),
            self.getGenero(),
            self.getDuracionFormato(),
            str.format("$%,.2f", self.precioObra(self.nombre)) + "\n",
        )
    
    @classmethod    
    def buscarObra(cls, nombre):
        from baseDatos.Teatro import Teatro
        return next(
            (
                obra
                for obra in Teatro.getInstancia().getObras()
                if obra.getNombre().lower() == nombre.lower()
            ),
            None,
        )

    def precioObra(self, nombre):
        from baseDatos import Teatro
        return next(
            (
                obra.precioFuncion()
                for obra in Teatro.getInstancia().getObras()
                if obra.getNombre().lower() == nombre.lower()
            ),
            0,
        )

    @staticmethod
    def nombres(cls, nombre):
        from baseDatos import Teatro
        listaNombres= []
        listaNombres.extend(
            obra.getNombre().lower() for obra in Teatro.getInstancia().getObras()
        )
        return nombre not in listaNombres

    @staticmethod
    def actualizarEstadoCritico(cls): 
        from baseDatos import Teatro
        for obra in Teatro.getInstancia().getObras():
            if obra.checkEstadoCritico():
                cls.estadoCriticoS.append(obra)
    
    @classmethod
    def mostrarObrasCriticas(cls):
        from baseDatos.Teatro import Teatro
        obrasCriticas = []
        obrasCriticas.extend(
            obra
            for obra in Teatro.getInstancia().getObras()
            if obra.promedioCalificacion() <= 2.0 and obra.getNombre() != "NOTFORITE"
        )
        return obrasCriticas

    def calcPromedioArt(self, reparto):
        i = 0
        f = 0
        if len(reparto) > 0:
            for actor in reparto:
                i = i + 1
                f = f + actor.getCalificacion()
        else:
            i = 1
        return f / i
    
    def isRepartoDisponible(self, inicio, fin):
        genteDisponibleFR = []
        for actor in self.getReparto():
            if actor.isDisponible(inicio, fin):
                genteDisponibleFR.append(actor)

        if len(genteDisponibleFR) == len(self.getReparto()):
            self.reparto = True
            return True
        else:
            self.reparto = False
            return False

    def addFuncion(self, funcion):
        self.funcionesSemana.append(funcion)

    @staticmethod
    def generarTabla():

        nuevo=""
        for obra in Teatro.getInstancia().getObras():
            if obra.getNombre() != "NOTFORITE":
                string = str.format("%30s %20s %20s %20s",obra.getNombre(),obra.getGenero(),
                                    obra.getDuracionFormato(),str.format("$%,.2f",
                                    obra.precioObra(obra.getNombre()))+"\n")
                nuevo = nuevo +string
        return nuevo
    @staticmethod
    def generarTabla1():
        nuevo = string = "{:>30} {:>20} {:>20} {:>20}".format(
                    "Nombre", "Genero","Duracion","Precio"
                )+ "\n"

        for obra in Teatro.getInstancia().getObras():
            if obra.getNombre() != "NOTFORITE":
                string = "{:>30} {:>20} {:>20} {:>20}".format(
                    obra.getNombre(), "comedia","10:00","1_000"
                ) + "\n"
                nuevo += string

        return nuevo

    def getDuracionFormato(self):
        horas = self.getDuracion().total_seconds() // 3600
        minutos = (self.getDuracion.total_seconds() % 3600) // 60
        return str.format("%d:%02d", horas, minutos)
    
    def getDuracionFormatoS(self):
        if not isinstance(self.getDuracion(), float):
            return datetime.timedelta(seconds= (self.getDuracion().total_seconds()))
        else:
            return datetime.timedelta(seconds=self.traducirDuracion())
    def addFuncion(self, funcion):
        self.getFuncionesSemana().append(funcion)
    
    def traducirDuracion(self):
        duracion = self.getDuracion()
        horas = duracion // 10000
        minutos = (duracion % 10000) // 100
        segundos = duracion % 100
        return horas * 3600 + minutos * 60 + segundos