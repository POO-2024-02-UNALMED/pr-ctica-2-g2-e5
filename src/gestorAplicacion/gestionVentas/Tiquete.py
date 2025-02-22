
from datetime import datetime
import random

from baseDatos.Teatro import Teatro
from gestorAplicacion.gestionVentas.Cliente import Cliente

class Tiquete:

    def __init__(self, valor: float = 0.0, id: int = 0, cliente=None, funcion=None,
                 personaje=None, obra=None, silla=None):
        self.valor = valor
        self.__id = id
        self.cliente = cliente
        self.funcion = funcion
        self.personaje = personaje
        self.obra = obra
        self.silla = silla
        Teatro.getInstancia().getTiquetes().append(self)
        

    def setId(self,id):
        self.__id=id

    def getId(self):
        return self.__id

    @staticmethod
    def idTiquete() -> int:
        while True:
            codigo = random.randint(0, 998)
            if not Tiquete.verificar(codigo):
                return codigo
    def verificar(elemento):
        for i in Tiquete.tiquetes:
            if i.getId==elemento:
                return True
        return False
    from datetime import datetime

    @staticmethod
    def imprimirFactura(cliente, b=False, d=10, p=0, su=0):
        precioTotal = p*d
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        


        cliente.getTiquete().setId(Tiquete.idTiquete())
        
        s = "================================\n"
        s += f"Tiquete # {cliente.getTiquete().getId()}\n"
        s += f"{fecha_actual}\n"
        s += "================================\n"
        s += f"{'Producto':<10}{'Precio':>20}\n"
        s += "--------------------------------\n"
        s += f"{'Funcion':<10}{'$' + format(precioTotal, ',.2f'):>20}\n"
        if not b and cliente.get_suscripcion().value != "Basica":
            s += f"{'Suscripcion':<10}{'$' + format(su, ',.2f'):>20}\n"
            s += f"{cliente.get_suscripcion().value:<25}\n"
        
        if cliente.get_suscripcion().name != "Basica":
            s += f"\nDescuento por ser {cliente.get_suscripcion().value}"
            s += f"\n-{format(p-precioTotal, ',.2f')}\n"
        


        s += "================================\n"
        s += "GRACIAS POR SU COMPRA\n"
        s += "================================\n"

        return s

        
                
