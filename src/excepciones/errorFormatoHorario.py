from excepciones.errorEntrada import errorEntrada

class errorFormatoHorario(errorEntrada):
    def __init__(self):
        super().__init__("El horario no está en el formato correcto")