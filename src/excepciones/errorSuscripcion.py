from excepciones.errorAplicacion import errorAplicacion

class errorSuscripcion(errorAplicacion):
    def __init__(self, mensaje = ""):
        super().__init__("Tu suscripcion no te permite comprar sillas tipo " + mensaje)