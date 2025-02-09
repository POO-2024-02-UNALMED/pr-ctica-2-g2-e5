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
                    while inicioFranjaITE < self.obra.franjaHoraria[1] and inicioFranjaITE + self.obra.getDuracionFormatoS()<(datetime.of(22,00)):
                        i = datetime.of(day, inicioFranjaITE)
                        v = i + self.obra.getDuracionFormatoS()
                        if self.obra.isRepartoDisponible(i, v) and sala.isDisponible(i,v):
                            horario.append(i)
                            horario.append(v)
                            self.sala = sala
                            self.sala.anadirHorario(horario);
                            return horario;
                        inicioFranjaITE = inicioFranjaITE.plusMinutes(30);
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

    def indiceFuncion(i, nombre){
    int in =0;
    
    for (Funcion funcion : Teatro.getInstancia().getFuncionesCreadas()) {
        if (funcion.obra!=null){
        if ((funcion.obra.getNombre().toLowerCase()).equals(nombre.toLowerCase())){
            in++;

        }
    }}

return in >= i;
}

public static Funcion escogerFuncion(int i,String nombre){
    int in=0;
    for (Funcion funcion : Teatro.getInstancia().getFuncionesCreadas()) {
        if (funcion.obra!=null){
        if ((funcion.obra.getNombre().toLowerCase()).equals(nombre.toLowerCase())){
            in++;
            if (in==i){
                return funcion;
            }
        }
            
        }
        
    }
    return null;

}
public static boolean calificacionVacia(Obra obra){
    boolean valor = true;
    if (obra.getCalificaciones().size()==0) {
        valor = false;
    }
    return valor;
    

}

    public static float precioFuncion(Funcion funcion){
        float prom = funcion.obra.promedioCalificacion();
        float precioBase=10000;
        float ad = (funcion.obra.getAsistencia()*500);
        if (prom > 8) {
            precioBase =( precioBase +(prom*800)+ad);
            
        } else if(prom > 5)
        {
            precioBase = (precioBase +(prom*400)+ad);
        } else if (prom > 3){
            precioBase = (precioBase +(prom*200+ad));
        }else{
            precioBase = (precioBase +(prom*100+ad));
        }
        
        

        return precioBase;

    }

public static String imprimirFuncion(Funcion funcion){
        String string = String.format("%30s %15s %10s %20s",funcion.obra.getNombre(),funcion.obra.getGenero(),funcion.obra.getDuracion().toMinutes(),String.format("$%,.2f",precioFuncion(funcion)));
        return string;
    }
    


public static Funcion buscarFuncion(String nombre){
    for (Funcion funcion : Teatro.getInstancia().getFuncionesCreadas()) {
        if (funcion.obra!=null){
        if ((funcion.obra.getNombre().toLowerCase()).equals(nombre.toLowerCase())){
            return funcion;
        }
        
    }}
    return null;


}

public static float mostrarPrecioFuncion(String nombre){
    for (Funcion funcion : Teatro.getInstancia().getFuncionesCreadas()) {
        if (funcion.obra!=null){
        if ((funcion.obra.getNombre().toLowerCase()).equals(nombre.toLowerCase())){
            return precioFuncion(funcion);
        }
    }
    }
    return 0;


}



public static boolean nombres(String nombre){
    ArrayList<String> listaNombres=new ArrayList<>();
    for (Funcion a : Teatro.getInstancia().getFuncionesCreadas()) {
        listaNombres.add(a.obra.getNombre().toLowerCase());
        
    }
    if(listaNombres.contains(nombre)){
        return false;

    }
    return true;



public  boolean verificar(long elemento){
    for (int i=0; i < sillas.size();i++){
        if (sillas.get(i).getCodigo()==elemento) {
            return false;
            
        }
        
    }
    return true;
}

public Silla asignarSilla(float elemento){
    for (int i=0; i < sillas.size();i++){
        if (sillas.get(i).getCodigo()==elemento) {
            return sillas.get(i);
        }
        
    }
    return sillas.get(0);

}

public String asignarTipoSilla(long elemento){
    for (int i=0; i < sillas.size();i++){
        if (sillas.get(i).getCodigo()==elemento) {
            return ""+sillas.get(i).getTipo().name().charAt(0);
            
        }
        
    }
    return ""