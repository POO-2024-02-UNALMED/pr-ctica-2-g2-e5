class CuentaBancaria:
    def __init__(self, idTitular, Saldo):
        self.idTitular = idTitular
        self.Saldo = Saldo

    def ingresar (self, cant):
        self.Saldo += cant

    def retirar(self, cant):
        if(cant > self._Saldo):
             return False
        else:
            self.Saldo = self.Saldo - cant
            return True
    
    def transferencia(self, Destino, cant):
        if(cant <= self._Saldo):
            self.retirar(cant)
            Destino.ingresar(cant)
            return True
        else:
            return False
        
            