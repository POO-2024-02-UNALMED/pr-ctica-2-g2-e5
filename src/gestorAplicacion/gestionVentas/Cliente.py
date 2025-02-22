from __future__ import annotations
import random
from baseDatos.Teatro import Teatro
from excepciones.errorSuscripcion import errorSuscripcion
from gestorAplicacion.gestionObras.Actor import Actor
from gestorAplicacion.herramientas.Persona import Persona


class Cliente(Persona):

    def __init__(self, obra: str = None, suscripcion = None, id: int = None, genero_favorito= None, actor_favorito= None, 
                 correo: str= None, tipo: str= None, cuenta_bancaria= None, tiquete= None):
        self.obra = obra
        self.__suscripcion = suscripcion
        self.__id = id
        self.genero_favorito = genero_favorito
        self.actor_favorito = actor_favorito
        self.ultimas_compras = []
        self.__historial = []
        self.correo = correo
        self.__tipo = tipo
        self.__cuentaBancaria = cuenta_bancaria
        self.__tiquete = tiquete
        Teatro.getInstancia().getClientes().append(self)


    #Debe ser reemplazada por buscarId en main
    def verificar(elemento):
        for i in Teatro.getInstancia().getClientes():
            if i.getId()==elemento:
                return True
        return False
    
    def verificarSuscripcion(self, s):
        a = 0
        b = 0
        
        # Asignación de valores a 'b' según la suscripción ingresada
        if s == "G":
            b = 3
        elif s == "P":
            b = 2
        elif s == "C":
            b = 1
        elif s == "B":
            b = 0
        
        # Asignación de valores a 'a' según la suscripción del cliente
        if self.get_suscripcion().value == "Basica":
            a = 0
        elif self.get_suscripcion().value  == "Premium":
            a = 1
        elif self.get_suscripcion().value  == "Vip":
            a = 2
        elif self.get_suscripcion().value  == "Elite":
            a = 3

        if  (a >=b):
            return True
        else:
            raise errorSuscripcion()
        
    @staticmethod
    def buscarPorId(id: int) -> Cliente | bool:
        for cliente in Teatro.getInstancia().getClientes():
            if cliente.getId() == id:
                return cliente
        return False
    
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
    
    def setId(self, value: int) -> None:
        self.__id = value

    def getTiquete(self):
        return self.__tiquete
    
    def setTiquete(self, value: int) -> None:
        self.__tiquete = value
    
    
    def set_suscripcion(self,susc):
        self.__suscripcion=susc

    def get_suscripcion(self):
        return self.__suscripcion
    
    def getTipo(self):
        return self.__tipo
    
    def getHistorial(self):
        return self.__historial
    
    def getCuentaBancaria(self):
        return self.__cuentaBancaria
    
    def pagarContratoActor(self, actor: Actor, precio: float) -> bool:

        if self.__tipo != "Empresa":
            return False
        
        if actor not in self.__historial:
            self.__historial.append(actor)

        transf = self.__cuentaBancaria.transferencia(Teatro.getInstancia().getTesoreria().getCuenta(), precio)
        
        if transf:
            return True
        else:
            return False



        

    
    

    