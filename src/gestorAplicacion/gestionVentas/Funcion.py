import datetime
from random import Random
import random

from baseDatos.Teatro import Teatro

class Funcion:

    def __init__(self, obra = None, tiquetesVendidos = 0, horario = [], sillas = [], sala = None, calificador = False,
            audienciaEsperada = 0, trabajador = False, asistentes = [], precio = 0.0, week = []):
        self.__obra = obra
        self.__tiquetesVendidos = tiquetesVendidos
        self.__horario = horario
        self.__sala = sala
        self.__calificador = calificador
        self.__audienciaEsperada = audienciaEsperada
        self.__trabajador = trabajador
        self.__asistentes = asistentes
        self.__precio = precio
        self.__sillas  = sala.get_sillas()
        Teatro.getInstancia().getFuncionesCreadas().append(self)
        
        if len(week)>0:
            self.__horario = self.createHorario(week)
            self.__sala = self.getSala()
            self.__audienciaEsperada = obra.getAudienciaEsperada()
            if self.__sala != None:
                self.__sillas = self.__sala.getSillas()        
    def getObra(self):
        return self.__obra
    
    def setObra(self, obra):
        self.__obra = obra
        
    def getTiquetesVendidos(self):
        return self.__tiquetesVendidos
    
    def setTiquetesVendidos(self, tiquetesVendidos):
        self.__tiquetesVendidos = tiquetesVendidos
        
    def getHorario(self):
        return self.__horario
    
    def setHorario(self, horario):  
        self.__horario = horario
        
    def getSillas(self):
        return self.__sillas
    
    def setSillas(self, sillas):
        self.__sillas = sillas
        
    def getSala(self):
        return self.__sala
    
    def setSala(self, sala):
        self.__sala = sala
        
    def getCalificador(self):
        return self.__calificador
    
    def setCalificador(self, calificador):
        self.__calificador = calificador
        
    def getAudienciaEsperada(self):
        return self.__audienciaEsperada
    
    def setAudienciaEsperada(self, audienciaEsperada):
        self.__audienciaEsperada = audienciaEsperada
        
    def getTrabajador(self):
        return self.__trabajador
    
    def setTrabajador(self, trabajador):    
        self.__trabajador = trabajador
        
    def getAsistentes(self):
        return self.__asistentes
    
    def setAsistentes(self, asistentes):
        self.__asistentes = asistentes
        
    def getPrecio(self):
        return self.__precio
    
    def setPrecio(self, precio):
        self.__precio = precio

    def tablaSillas(self):
        Nuevo=""
        sillas = self.getSala().getSillas()
        for i in range(len(sillas)):    
            if (sillas[i].getCodigo() != 88):
                Nuevo = f"{Nuevo}        "
            else:
                primerCaracter = sillas[i].getTipo().name().charAt(0)
                Nuevo=Nuevo+primerCaracter+"-"+str.format("%04d", sillas[i].getCodigo())+"  "

            if ((i + 1) % 8 == 0):
                Nuevo = Nuevo+"\n"

        return Nuevo+"\n\n-ESCENARIO-"

    def eliminarSilla(self, i):
        from gestionVentas import Silla
        sillaVacia = Silla(codigo = 88)
        sillas = self.getSala().getSillas()
        for k in range (len(sillas)):
            if sillas[k].getCodigo() == i:
                sillas[k] = sillaVacia

    def salaDisponible(self, sala):
        return sala
    
    @staticmethod
    def actualizarFuncionesVenta(cls, funcionesCreadas):
        if len(funcionesCreadas) > 0:
            funcionesALaVenta = []
            for funcion in funcionesCreadas:
                if len(funcion.getHorario()) <= 0:
                    break
                if funcion.getHorario()[0] > datetime.now():
                    funcionesALaVenta.append(funcion)

            return funcionesALaVenta

    def createHorario(self, week):
        from baseDatos import Teatro
        import datetime
        horario = []
        inicioFranja = self.getObra().getFranjaHoraria()[0]
        for sala in Teatro.getInstancia().getSalas():
            if sala.getCapacidad() > self.getObra().getAudienciaEsperada():
                for day in week:
                    inicioFranjaITE = inicioFranja
                    while inicioFranjaITE < self.getObra().getFranjaHoraria()[1] and inicioFranjaITE + self.getObra().getDuracionFormatoS()<(datetime.datetime(22,00)):
                        i = datetime.datetime(day, inicioFranjaITE)
                        v = i + self.getObra().getDuracionFormatoS()
                        if self.getObra().isRepartoDisponible(i, v) and sala.isDisponible(i,v):
                            horario.extend((i, v))
                            self.setSala(sala) 
                            self.getSala().anadirHorario(horario)
                            return horario
                        inicioFranjaITE = inicioFranjaITE.total_minutes() + 30
        return horario

    def extraerHora(self):
        horario = self.getHorario()
        for tiempo in horario:
            hora = tiempo.total_hours()
            minutos = tiempo.total_minutes()
            segundos = tiempo.total_seconds()
        return [datetime.datetime(hora, minutos, segundos)]
    
    def doWeNeedACalificador(self):
        a = False
        for actor in self.getObra().getReparto():
            if actor.getReevaluacion():
                a = True
        return a

    @staticmethod
    def generarTabla(cls, nombre):
        from baseDatos import Teatro
        il = 0
        Nuevo = ""
        string =""
        for funcion in Teatro.getInstancia().getFuncionesCreadas():
            if funcion.obra != None and funcion.obra.nombre != None and funcion.obra.getNombre().toLowerCase() == nombre.toLowerCase() and funcion.getObra().getNombre() != "NOTFORITE":
                il += 1
                string = f"{il:20} {funcion.obra.getNombre():30} {funcion.getHorario()[0]}"
                Nuevo = Nuevo + "\n" + string
        return Nuevo

    def indiceFuncion(self, i, nombre):
        from baseDatos import Teatro
        il = 0
        for funcion in Teatro.getInstancia().getFuncionesCreadas():
            if funcion.obra != None and (funcion.obra.nombre.lower()) == nombre.lower():
                il = il + 1
        return il >= i

    def escogerFuncion(self, i, nombre):
        from baseDatos import Teatro
        il = 0
        for funcion in Teatro.getInstancia().getFuncionesCreadas():
            if funcion.obra!=None and funcion.obra.nombre.lower() == nombre.lower():
                il = il + 1
            if il==i:
                return funcion
        return None

    def calificacionVacia(self, obra):
        return obra.califcacionVacia()

    def precioFuncion(self):
        prom = random.randint(1,10)
        precioBase = 10000
        ad = 0
        if prom > 8:
            return precioBase + prom * 800 + ad  * 500
        elif prom > 5:
            return precioBase + prom * 400 + ad
        elif prom > 3:
            return precioBase + prom * 200 + ad
        else:
            return precioBase + prom * 100 + ad

    def imprimirFuncion(self):
        return str.format(
            "%30s %15s %10s %20s",
            self.obra.nombre,
            self.obra.genero,
            self.obra.duracion.total_minutes(),
            str.format("$%,.2f", self.precioFuncion()),
        )
    

    @staticmethod
    def buscarFuncion(cls, nombre):
        from baseDatos import Teatro
        return next(
            (
                funcion
                for funcion in Teatro.getInstancia().getFuncionesCreadas()
                if funcion.obra != None
                and funcion.obra.nombre.lower() == nombre.lower()
            ),
            None,
        )

    @staticmethod
    def mostrarPrecioFuncion(cls, nombre):
        from baseDatos import Teatro
        for funcion in Teatro.getInstancia().getFuncionesCreadas():
            if funcion.obra != None:
                if funcion.obra.nombre.lower() == nombre.lower():
                    return funcion.precioFuncion()
        return 0

    @staticmethod
    def nombres(cls, nombre):
        from baseDatos import Teatro
        listaNombres = []
        for funcion in Teatro.getInstancia().getFuncionesCreadas():
            listaNombres.append(funcion.obra.nombre.lower())
        if  nombre in listaNombres:
            return False
        else: 
            return True

    def verificar(self, elemento):
        for i in len(self.sillas):
            if self.sillas[i].codigo == elemento:
                return False
            else:
                return True

    def asignarSilla(self, elemento):
        for i in len(self.sillas):
            if self.sillas[i].codigo == elemento:
                return self.sillas[i]
        return self.sillas[0]

    def asignarTipoSilla(self, elemento):
        for i in len(self.sillas):
            if (self.sillas[i].codigo == elemento):
                return ""+self.sillas.get[i].tipo.name().charAt(0)
        return ""