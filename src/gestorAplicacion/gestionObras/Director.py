from gestorAplicacion.gestionObras.Artista import Artista
class Director(Artista):

    def __init__(self, nombre = "", id = 0, genero = None):
        from baseDatos.Teatro import Teatro
        self.genero = genero
        self.horario = []
        super().__init__(nombre, id)
        Teatro.getInstancia().getDirectors().append(self)
        Teatro.getInstancia().getArtistas().append(self)
    
    def str(self):
        return "Nombre: " + self.nombre + "\n" + "Identificación: " + self.id + "\n" + "Género: " + self.genero
