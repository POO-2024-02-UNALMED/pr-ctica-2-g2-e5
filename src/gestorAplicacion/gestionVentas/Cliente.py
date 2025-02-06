

class Cliente:

    clientes = []  # Lista estática de clientes

    def __init__(self, obra: str = None, suscripcion = None, id: int = 0, genero_favorito= None, actor_favorito= None, 
                 correo: str= None, tipo: str= None, cuenta_bancaria= None, tiquete= None):
        self.obra = obra
        self.suscripcion = suscripcion
        self.id = id
        self.genero_favorito = genero_favorito
        self.actor_favorito = actor_favorito
        self.ultimas_compras = []
        self.historial = []
        self.correo = correo
        self.tipo = tipo
        self.cuenta_bancaria = cuenta_bancaria
        self.tiquete = tiquete
        Cliente.clientes.append(self)  # Agregar instancia a la lista de clientes

    
    

    