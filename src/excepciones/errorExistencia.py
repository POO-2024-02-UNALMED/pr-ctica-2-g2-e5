from excepciones.errorAplicacion import errorAplicacion

class errorExistencia(errorAplicacion):
    def __init__(self, mensaje = ""):
        super().__init__("No hay existencias." + mensaje)
