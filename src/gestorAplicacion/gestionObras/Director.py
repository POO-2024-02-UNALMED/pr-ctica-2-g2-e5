from gestionObras import Artista
class Director(Artista):
    directors = []
    def __init__(self, nombre = "", id = 0, genero = None):
        from baseDatos import Teatro
        self.genero = genero
        self.horario = []
        super.__init__(nombre, id)
        Teatro.getInstancia().directors.append(self)
        Teatro.getInstancia().artistas.append(self)
        Director.directors.append(self)
        genero.anadirDirector(self)
    
    def str(self):
        return "Nombre: " + self.nombre + "\n" + "Identificación: " + self.id + "\n" + "Género: " + self.genero
    
    def isDisponible(self, inicio, fin):
        for evento in self.horario:
            if inicio < evento[1] and fin > evento[0]:
                return False
                pass
        return True 
