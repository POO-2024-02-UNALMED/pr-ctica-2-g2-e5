

class Tiquete:

    tiquetes = []  # Lista estática de tiquetes

    def __init__(self, valor: float = 0.0, id: int = 0, cliente=None, funcion=None,
                 personaje=None, obra=None, silla=None):
        self.valor = valor
        self.id = id
        self.cliente = cliente
        self.funcion = funcion
        self.personaje = personaje
        self.obra = obra
        self.silla = silla
        Tiquete.tiquetes.append(self)  # Agregar instancia a la lista de tiquetes
