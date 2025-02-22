from excepciones.errorExistencia import errorExistencia

class errorIdExiste(errorExistencia):
    def __init__(self):
        super().__init__("El id ya esta asociado a otro usuario")