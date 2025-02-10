class CuentaBancaria:
    pass
    def __init__(self, idTitular, Saldo):
        self.__idTitular = idTitular
        self.__Saldo = Saldo
    def ingresar (self, cant):
        self.__Saldo += cant
    def retirar(self, cant):
        if(cant > self.__Saldo):
             return False
        else:
            self.__Saldo = self.__Saldo - cant
            return True
    
    def transferencia(self, Destino, cant):
        if(cant <= self.__Saldo):
            self.retirar(cant)
            Destino.ingresar(cant)
            return True
        else:
            return False
        
    # Getters and Setters
    def getIdTitular(self):
        return self.__idTitular
    def setIdTitular(self, idTitular):
        self.__idTitular = idTitular
    def getSaldo(self):
        return self.__Saldo
    def setSaldo(self, Saldo):
        self.__Saldo = Saldo
            