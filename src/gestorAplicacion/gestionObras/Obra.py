class Obra:
        self.costoProduccion = 0
        self.funcionesSemana = []
        self.genero = null;
        self.tiquetesTotales = 0
        self.estadoCriticoA = null
        self.calificaciones = []
        self.franjaHoraria = []
        self.duracion = null
        self.funcionEstelar = null
        self.funciones = []
        self.funcionesRecomendadas = 0
        self.promedioArt = 0
        self.repartoDisponible = false
        self.asistencia = 0
        self.precio = 0
        self.calcularCalificacion(calificaciones)
        self.calcAudienciaEsperada(calificacion)
    def funcionesRecomendadas(promedioArt):
        if promedioArt < 2:
            return 3
        elif promedioArt >= 2 and promedioArt < 3:
            return 5
        elif promedioArt >= 3 and promedioArt < 4:
            return 7
        else:
            return 10
    def calcAudienciaEsperada(calificacion):
        u = calificacion * 12
        self.audienciaEsperada = u
    def calcularCalificacion(calificaciones):
        u = 0
        t = 0
        for i in calificaciones:
            u = u + i
            t++
        v = u / t
        self.calificacion = v
    def franjaHoraria(genero):
        a = Funcion(datetime(2024,1,02,00,00))
        franja = [time(00,00),time(23,59)]
        obrasGenero = []
        for obra in Teatro.instancia.obras:
            u = obra.genero
            if u == genero:
                obrasGenero.append(obra)
        for obra in obrasGenero:
            a = obra.funcionEstelar
            if a != null:
                fstar = a.extraerHora(a.horario)
                if fstar.size() >= 2:
                    if fstar[0] > franja[0]:
                        franja[0] = fstar[0]
                    if fstar[1] < franja[1]:
                        franja[1] = fstar[1]
            else:
                pass
        self.franjaHoraria = franja
    pass