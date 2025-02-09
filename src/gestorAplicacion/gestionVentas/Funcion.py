import datetime

class Funcion:
    funcionesCreadas = []  # Lista estática de funciones creadas
    funcionesALaVenta = []  # Lista estática de funciones a la venta

    def __init__(self, obra = None, tiquetesVendidos = 0, horario = [], sillas = [], sala = None, calificador = False,
                 audienciaEsperada = 0, trabajador = False, asistentes = [], precio = 0.0):
        self.obra = obra
        self.tiquetesVendidos = tiquetesVendidos
        self.horario = horario
        self.sillas  = sillas
        self.sala = sala
        self.calificador = calificador
        self.audienciaEsperada = audienciaEsperada
        self.trabajador = trabajador
        self.asistentes = asistentes
        self.precio = precio
        Funcion.funcionesCreadas.append(self)

    def tablaSillas(self):
        Nuevo=""
        sillas = self.sala.sillas
        for  i in range(len(sillas)):        
            if (sillas[i].codigo != 88):
                Nuevo=Nuevo+"        "
            else:
                primerCaracter = sillas[i].tipo.name().charAt(0)
                Nuevo=Nuevo+primerCaracter+"-"+str.format("%04d", sillas[i].codigo)+"  "

            if ((i + 1) % 8 == 0):
                Nuevo = Nuevo+"\n"

        return Nuevo+"\n\n-ESCENARIO-"

    def eliminarSilla(self, i):
        from gestionVentas import Silla
        sillaVacia = Silla(codigo = 88)
        sillas = self.sala.sillas
        for k in range (len(sillas)):
            if sillas[k].codigo == i:
                sillas[k] = sillaVacia

    def salaDisponible(self, sala):
        return sala
    
    def actualizarFuncionesVenta(cls, funcionesCreadas):
        funcionesALaVenta = []
        if len(funcionesCreadas) > 0:
            for funcion in funcionesCreadas:
                if len(funcion.horario) > 0:
                    if funcion.horario[0] > datetime.now():
                        funcionesALaVenta.append(funcion)

                else:
                    break
            return funcionesALaVenta

    def createHorario(self, week):
        from baseDatos import Teatro
        import datetime
        horario = []
        inicioFranja = self.obra.franjaHoraria[0]
        for sala in Teatro.getInstancia().getSalas():
            if sala.capacidad > self.obra.audienciaEsperada:
                for day in week:
                    inicioFranjaITE = inicioFranja
                    while inicioFranjaITE < self.obra.franjaHoraria[1] and inicioFranjaITE + self.obra.getDuracionFormatoS()<(datetime.datetime(22,00)):
                        i = datetime.datetime(day, inicioFranjaITE)
                        v = i + self.obra.getDuracionFormatoS()
                        if self.obra.isRepartoDisponible(i, v) and sala.isDisponible(i,v):
                            horario.append(i)
                            horario.append(v)
                            self.sala = sala
                            self.sala.anadirHorario(horario)
                            return horario
                        inicioFranjaITE = inicioFranjaITE.total_minutes() + 30
        return horario

    def extraerHora(self, horario):
        a = []
        for tiempo in horario:
            hora = tiempo.total_hours()
            minutos = tiempo.total_minutes()
            segundos = tiempo.total_seconds()
        a.append(datetime.datetime(hora, minutos, segundos))
        return a
    
    def doWeNeedACalificador(self):
        a = False
        for actor in self.obra.reparto:
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

    def indiceFuncion(sekf, i, nombre):
        from baseDatos import Teatro
        il = 0
        for funcion in Teatro.getInstancia().getFuncionesCreadas():
            if funcion.obra != None:
                if (funcion.obra.nombre.lower()) == nombre.lower():
                    il = il + 1
        return il >= i

    def escogerFuncion(self, i, nombre):
        from baseDatos import Teatro
        il = 0
        for funcion in Teatro.getInstancia().getFuncionesCreadas():
            if funcion.obra!=None:
                if funcion.obra.nombre.lower() == nombre.lower():
                    il = il + 1
            if il==i:
                return funcion
        return None

    def calificacionVacia(self, obra):
        return obra.califcacionVacia()

    def precioFuncion(self):
        prom = self.obra.promedioCalificacion()
        precioBase = 10000
        ad = self.obra.asistencia*500
        if prom > 8 :
            precioBase = precioBase + prom * 800 + ad  * 500        
        elif prom > 5:
            precioBase = precioBase + prom * 400 + ad
        elif prom > 3:
            precioBase = precioBase + prom * 200 + ad
        else:
            precioBase = precioBase + prom * 100 + ad
        return precioBase

    def imprimirFuncion(self):
        string = str.format("%30s %15s %10s %20s",self.obra.nombre,self.obra.genero,self.obra.duracion.total_minutes(),str.format("$%,.2f",self.precioFuncion()))
        return string
    

    @staticmethod
    def buscarFuncion(cls, nombre):
        from baseDatos import Teatro
        for funcion in Teatro.getInstancia().getFuncionesCreadas():
            if funcion.obra!=None:
                if funcion.obra.nombre.lower() == nombre.lower():
                    return funcion
        return None

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