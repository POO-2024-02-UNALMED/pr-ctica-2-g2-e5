class CuentaBancaria:
    def __init__(self, idTitular, Saldo):
        self._idTitular = idTitular
        self._Saldo = Saldo

    def ingresar (self, cant):
        self._Saldo += cant

    def retirar(self, cant):
        if(cant > self._Saldo):
             return False
        else:
            self._Saldo = self._Saldo - cant
            return True
    
    def transferencia(self, Destino, cant):
        if(cant <= self._Saldo):
            self.retirar(cant)
            Destino.ingresar(cant)
            return True
        else:
            return False
        
    # Getters and Setters

    def getIdTitular(self):
        return self._idTitular

    def setIdTitular(self, idTitular):
        self._idTitular = idTitular

    def getSaldo(self):
        return self._Saldo

    def setSaldo(self, Saldo):
        self._Saldo = Saldo
            