from enum import Enum

class Genero(Enum):
    DRAMA = object()
    COMEDIA = object()
    MUSICAL = object()
    FANTASIA = object() 
    TERROR = object() 
    ROMANCE = object() 
    CIRCO = object() 
    EXPERIMENTAL = object()

    def __init__(self, directores):
        directores = self.getDirectores()
        
    def getDirectores(self):
        from baseDatos import Teatro
        dirgenero = []
        for director in Teatro.getInstancia().getDirectors():
            if director.genero == self:
                dirgenero.append(director)
            return dirgenero

    def anadirDirector(self, director):
        self.directores.append(director)