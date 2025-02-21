from excepciones.errorAplicacion import errorAplicacion

class errorEntrada(errorAplicacion):
    def __init__(self, mensaje = ""):
        super().__init__("Entrada rellenada de forma inválida. " + mensaje)