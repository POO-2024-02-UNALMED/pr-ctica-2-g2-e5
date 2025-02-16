

import random
from baseDatos.Teatro import Teatro


class Cliente:

    clientes = []  # Lista estática de clientes

    def __init__(self, obra: str = None, suscripcion = None, id: int = 0, genero_favorito= None, actor_favorito= None, 
                 correo: str= None, tipo: str= None, cuenta_bancaria= None, tiquete= None):
        self.obra = obra
        self.suscripcion = suscripcion
        self.__id = id
        self.genero_favorito = genero_favorito
        self.actor_favorito = actor_favorito
        self.ultimas_compras = []
        self.__historial = []
        self.correo = correo
        self.__tipo = tipo
        self.__cuentaBancaria = cuenta_bancaria
        self.tiquete = tiquete
        Teatro.getInstancia().getClientes().append(self)


    def verificar(elemento):
        for i in Cliente.clientes:
            if i.id==elemento:
                return True
        return False
    
    def verificar_suscripcion(self, s: str) -> bool:
        b = {"G": 3, "P": 2, "C": 1, "B": 0}.get(s, 0)
        
        suscripcion_niveles = {"Basica": 0, "Premium": 1, "Vip": 2, "Elite": 3}
        a = suscripcion_niveles.get(self.cliente.suscripcion.name if self.cliente and self.cliente.suscripcion else "Basica", 0)
        
        return not (a >= b)

    def asignar(id: int):
        for cliente in Cliente.clientes:
            if cliente.id == id:
                return cliente
        return None
    
    @staticmethod
    def id_random() -> int:
        while True:
            codigo = random.randint(0, 998)
            if not Cliente.verificar(codigo):
                return codigo
            
    def consultar_perfil(self) -> str:
        perfil = f"{'Usuario N.':>30} {self.id}\n"
        ultima_compra = f"{'Su ultima compra :':>30} {self.obra if self.obra else 'Ninguna'}\n"
        suscripcion = f"{'Su suscripcion es :':>30} {self.cliente.suscripcion if self.cliente and self.cliente.suscripcion else 'No especificada'}\n"
        
        return perfil + ultima_compra + suscripcion

    def getId(self):
        return self.__id
    
    def getTipo(self):
        return self.__tipo
    
    def getHistorial(self):
        return self.__historial
    
    def getCuentaBancaria(self):
        return self.__cuentaBancaria



        

    
    

    