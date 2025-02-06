from gestionFinanciera.CuentaBancaria import CuentaBancaria

class Tesoreria:
    def __init__(self, total, metaSemanal):
        self.dineroEnCaja = 0
        self.metaSemanal = metaSemanal
        self.cuenta = CuentaBancaria(1, 10000000)
        self.total = total
    
    def verificacionMeta(self):
        return self.__total >= self.__metaSemanal

    #Transferir dinero de la caja a la cuenta
    def transferenciaFondos(self):
        self.__cuenta.ingresar(self.__dineroEnCaja)
        self.__dineroEnCaja = 0
    
    #pagar el sueldo base
    def pagarSueldoBase(self, cuenta, cantidad):
        self.__cuenta.transferencia(cuenta, cantidad)
    
    