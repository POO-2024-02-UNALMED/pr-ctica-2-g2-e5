from gestorAplicacion.gestionFinanciera.CuentaBancaria import CuentaBancaria

class Tesoreria:

    def __init__(self, total, metaSemanal):
        self.__dineroEnCaja = 0
        self.__metaSemanal = metaSemanal
        self.__cuenta = CuentaBancaria(1, 10000000)
        self.__total = total
    
    #Permite verificar si el teatro cumplio con su obejetivo de ingresos
    def verificacionMeta(self):
        return self.__total >= self.__metaSemanal
    
    #Permite transferir todo el dinero recaudado en la caja a la cuenta del Teatro
    def transferenciaFondos(self):
        self.__cuenta.ingresar(self.__dineroEnCaja)
        self.__dineroEnCaja = 0
    
    #Hace el pago a la cuenta de los empleados solo con su sueldo base
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
    