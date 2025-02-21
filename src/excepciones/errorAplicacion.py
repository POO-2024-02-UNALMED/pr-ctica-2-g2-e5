class errorAplicacion(Exception):
    def __init__(self, mensaje):
        self.mensaje = "Error durante ejecución de la aplicación: " + mensaje
        super().__init__(self.mensaje)