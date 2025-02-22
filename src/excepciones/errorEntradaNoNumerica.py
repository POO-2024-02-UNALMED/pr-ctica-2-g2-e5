from excepciones.errorEntrada import errorEntrada

class errorEntradaNoNumerica(errorEntrada):
    def __init__(self):
        super().__init__("Existe una entrada ingresada que no puede convertirse a número")