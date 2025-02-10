from gestionFinanciera.CuentaBancaria import CuentaBancaria

class Tesoreria:
    pass
    def __init__(self, total, metaSemanal):
        self.__dineroEnCaja = 0
        self.__metaSemanal = metaSemanal
        self.__cuenta = CuentaBancaria(1, 10000000)
        self.__total = total
    
    def verificacionMeta(self):
        return self.__total >= self.__metaSemanal
    #Transferir dinero de la caja a la cuenta
    def transferenciaFondos(self):
        self.__cuenta.ingresar(self.__dineroEnCaja)
        self.__dineroEnCaja = 0
    
    #pagar el sueldo base
    def pagarSueldoBase(self, cuenta, cantidad):
        self.__cuenta.transferencia(cuenta, cantidad)
    
    #Getters and Setters
    def getDineroEnCaja(self):
        return self.__dineroEnCaja
    
    def setDineroEnCaja(self, dinero):
        self.__dineroEnCaja = dinero
    def getCuenta(self):
        return self.__cuenta
    
    def setCuenta(self, cuenta):
        self.__cuenta = cuenta
    
    def getTotal(self):
        return self.__total
    
    def setTotal(self, total):
        self.__total = total
    def getMetaSemanal(self):
        return self.__metaSemanal
    
    def setMetaSemanal(self, metaSemanal):
        self.__metaSemanal = metaSemanal
    