class errorAplicacion(Exception):
    def __init__(self):
        self.mensaje = "Error en la aplicación"
        super().__init__(self.mensaje)