import datetime
import time

class Obra:
    estadoCriticoS = []
    obras = []
    def __init__(self, audienciaEsperada = 0, nombre = "", calificacion = 0, reparto = [], papeles = [], director = None, costoProducción = 0, funcionesSemana = [], genero = None, tiquetesTotales = 0, estadoCriticoA = False, calificaciones = [], franjaHoraria = [],
                duracion = None, funcionEstelar = None, funciones = [], funcionesRecomendadas = 0, promedioArt = 0, repartoDisponible = False, asistencia = 0, precio = 0):
        self.audienciaEsperada = audienciaEsperada
        self.nombre = nombre
        self.calificacion = calificacion
        self.reparto = reparto
        self.papeles = papeles
        self.director = director
        self.costoProduccion = costoProducción
        self.funcionesSemana = funcionesSemana
        self.genero = genero
        self.tiquetesTotales = tiquetesTotales
        self.estadoCriticoA = estadoCriticoA
        self.calificaciones = calificaciones
        self.franjaHoraria = franjaHoraria
        self.duracion = duracion
        self.funcionEstelar = funcionEstelar
        self.funciones = funciones
        self.funcionesRecomendadas = funcionesRecomendadas
        self.promedioArt = promedioArt
        self.repartoDisponible = repartoDisponible
        self.asistencia = asistencia
        self.precio = precio
        self.calcularCalificacion(self.calificaciones)
        self.calcAudienciaEsperada(self.calificacion)
        self.checkEstadoCritico()
        Obra.obras.append(self)

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
        self.audienciaEsperada = u
    
    def calcularCalificacion(self, calificaciones):
        u = 0
        t = 0
        for i in calificaciones:
            u = u + i
            t = t+1
        v = u / t
        self.calificacion = v

    def franjaHoraria(self, genero):
        from gestionVentas import Funcion
        from baseDatos import Teatro
        a = Funcion(datetime(2024,1,2,00,00))
        franja = [time(00,00),time(23,59)]
        obrasGenero = []
        for obra in Teatro.getInstancia().getObras():
            u = obra.genero
            if u == genero:
                obrasGenero.append(obra)
        for obra in obrasGenero:
            a = obra.funcionEstelar
            if a != None:
                fstar = a.extraerHora(a.horario)
                if fstar.size() >= 2:
                    if fstar[0] > franja[0]:
                        franja[0] = fstar[0]
                    if fstar[1] < franja[1]:
                        franja[1] = fstar[1]
        self.franjaHoraria = franja

    def  calcFuncionEstelar(self,funciones):
        from gestionVentas import Funcion
        u = Funcion()
        v = Funcion()
        u.tiquetesVendidos = 0
        s = u.tiquetesVendidos
        for funcion in funciones:
            d = funcion.tiquetesVendidos
            if s < d:
                s = d
                v = funcion
        self.funcionEstelar = v

    def checkEstadoCritico(self):
        return self.calificacion < 1

    def calificacionVacia(self):
        return len(self.calificaciones) != 0

    def promedioCalificacion(self):
        suma=0
        contador = 0
        if self.calificacionVacia() == False :
            return 0
        for cal in  self.calificaciones:
            suma = suma + cal
            contador = contador + 1
        return (suma / contador)
        
    def recurrencia(self):
        self.asistencia = self.asistencia + 1
    
    def precioFuncion(self):
            prom = self.promedioCalificacion()
            precioBase = 10000
            ad = self.asistencia*500
            if prom > 8:
                precioBase = precioBase + prom * 800 + ad

            elif prom > 5:
                precioBase = precioBase + prom * 400 + ad
             
            elif prom > 3:
                precioBase = precioBase + prom * 200 + ad

            else:
                precioBase = precioBase + prom * 100 + ad
            
            self.precio(precioBase)

    def imprimirObra(self):
        return str.format(
            "%30s %20s %20s %20s",
            self.nombre,
            self.genero,
            self.getDuracionFormato(),
            str.format("$%,.2f", self.precioObra(self.nombre)) + "\n",
        )
        
    def buscarObra(self, nombre):
        from baseDatos import Teatro
        return next(
            (
                obra
                for obra in Teatro.getInstancia().getObras()
                if obra.nombre.lower() == nombre.lower()
            ),
            None,
        )

    def precioObra(self, nombre):
        from baseDatos import Teatro
        return next(
            (
                obra.precioFuncion()
                for obra in Teatro.getInstancia().getObras()
                if obra.nombre.lower() == nombre.lower()
            ),
            0,
        )

    @staticmethod
    def nombres(cls, nombre):
        from baseDatos import Teatro
        listaNombres= []
        listaNombres.extend(
            obra.nombre.lower() for obra in Teatro.getInstancia().getObras()
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
        from baseDatos import Teatro
        obrasCriticas = []
        obrasCriticas.extend(
            obra
            for obra in Teatro.getInstancia().getObras()
            if obra.promedioCalificacion() <= 2.0 and obra.nombre == "NOTFORITE"
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
        for actor in self.reparto:
            if actor.isDisponible(inicio, fin):
                genteDisponibleFR.add(actor)

        if len(genteDisponibleFR) == len(self.reparto):
            self.reparto = True
            return True
        else:
            self.reparto = False
            return False

    def addFuncion(self, funcion):
        self.funcionesSemana.append(funcion)

    @staticmethod
    def generarTabla(cls):
        from baseDatos import Teatro
        nuevo=""
        for obra in Teatro.getInstancia().getObras():
            if obra.nombre != "NOTFORITE":
                string = str.format("%30s %20s %20s %20s",obra.nombre,obra.genero,obra.getDuracionFormato(),str.format("$%,.2f",obra.precioObra(obra.nombre))+"\n")
                nuevo = nuevo +string
        return nuevo
    
    def getDuracionFormato(self):
        horas = self.duracion.total_seconds() // 3600
        minutos = (self.duracion.total_seconds() % 3600) // 60
        return str.format("%d:%02d", horas, minutos)
    
    def getDuracionFormatoS(self):
        return self.duracion.total_seconds()