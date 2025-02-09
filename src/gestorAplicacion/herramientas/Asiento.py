from enum import Enum

class Asiento(Enum):
        BASICO = object()
        COMFORT = object()
        PREMIUM = object()
        GOLD = object()

        def tipos():
            top = str.format("%30s %30s ","Tipo Asiento","Suscripcion necesaria\n\n")
            tipo1 = str.format("%30s %30s  ","BASICO","N/A\n")
            tipo2 = str.format("%30s %30s  ","COMFORT","PREMIUM\n")
            tipo3 = str.format("%30s %30s  ","PREMIUM","VIP\n")
            tipo4 = str.format("%30s %30s  ","GOLD","ELITE")
            return top+tipo1+tipo2+tipo3+tipo4
        
        def imprimirTipos(tipo):
            for asiento in Asiento.values():
                if (asiento.name().equalsIgnoreCase(tipo)):
                    return False 
            return True