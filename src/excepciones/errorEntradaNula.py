from excepciones.errorEntrada import errorEntrada

class errorEntradaNula(errorEntrada):
    def __init__(self):
        super().__init__("Existe por lo menos una entrada vacía")