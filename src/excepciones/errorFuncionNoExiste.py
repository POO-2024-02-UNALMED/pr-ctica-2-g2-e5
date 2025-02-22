from excepciones.errorExistencia import errorExistencia

class errorFuncionNoExiste(errorExistencia):
    def __init__(self):
        super().__init__("No hay funciones disponibles")