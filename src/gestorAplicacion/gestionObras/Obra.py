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
        elif promedioArt >= 2 and promedioArt < 3:
            return 5
        elif promedioArt >= 3 and promedioArt < 4:
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
            else:
                pass
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
        if self.calificacion < 1:
            return True
        else:
            return False

    def calificacionVacia(self):
        valor = True
        if len(self.calificaciones) == 0:
            valor = False
        return valor
             
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
            string = str.format("%30s %20s %20s %20s", self.getNombre(), self.getGenero(), self.getDuracionFormato(), str.format("$%,.2f", self.precioObra(self.nombre))+"\n")
            return string
        
    def buscarObra(self, nombre):
        from baseDatos import Teatro
        for obra in Teatro.getInstancia().getObras():
            if obra.nombre.lower() == nombre.lower():
                return obra
        return None

    def precioObra(self, nombre):
        from baseDatos import Teatro
        for obra in Teatro.getInstancia().getObras(): 
            if obra.nombre.lower() == nombre.lower():
                return obra.precioFuncion()
        return 0

    def nombres(cls, nombre):
        from baseDatos import Teatro
        listaNombres= []
        for obra in Teatro.getInstancia().getObras():
            listaNombres.append(obra.nombre.lower())

        if(nombre in listaNombres):
            return False
            pass
        return True

    def actualizarEstadoCritico(cls): 
        from baseDatos import Teatro
        for obra in Teatro.getInstancia().getObras():
            if obra.checkEstadoCritico():
                cls.estadoCriticoS.append(obra)
    
    def mostrarObrasCriticas(cls):
        from baseDatos import Teatro
        obrasCriticas = []
        for obra in Teatro.getInstancia().getObras():
            if obra.promedioCalificacion() <= 2.0 and obra.nombre == "NOTFORITE" :
                obrasCriticas.append(obra)
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

    def generarTabla(cls):
        from baseDatos import Teatro
        nuevo=""
        for obra in Teatro.getInstancia().getObras():
            if obra.nombre != "NOTFORITE":
                string = str.format("%30s %20s %20s %20s",obra.nombre,obra.genero,obra.getDuracionFormato(),str.format("$%,.2f",obra.precioObra(obra.nombre))+"\n")
                Nuevo = Nuevo +string
        return Nuevo
    