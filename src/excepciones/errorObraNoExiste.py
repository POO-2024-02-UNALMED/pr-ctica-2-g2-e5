from excepciones.errorExistencia import errorExistencia

class errorObraNoExiste(errorExistencia):
    def __init__(self):
        super().__init__("La obra no existe")