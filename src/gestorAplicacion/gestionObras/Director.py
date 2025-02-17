from gestorAplicacion.gestionObras.Artista import Artista
class Director(Artista):
    directors = []
    def __init__(self, nombre = "", id = 0, genero = None):
        from baseDatos.Teatro import Teatro
        self.genero = genero
        self.horario = []
        super().__init__(nombre, id)
        Teatro.getInstancia().getDirectors().append(self)
        Teatro.getInstancia().getArtistas().append(self)
        Director.directors.append(self)
       # genero.anadirDirector(self) Comentado por razones de prueba
    
    def str(self):
        return "Nombre: " + self.nombre + "\n" + "Identificación: " + self.id + "\n" + "Género: " + self.genero
