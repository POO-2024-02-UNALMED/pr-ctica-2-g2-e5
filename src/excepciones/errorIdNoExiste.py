from excepciones.errorExistencia import errorExistencia

class errorIdNoExiste(errorExistencia):
    def __init__(self):
        super().__init__("Id no encontrado")