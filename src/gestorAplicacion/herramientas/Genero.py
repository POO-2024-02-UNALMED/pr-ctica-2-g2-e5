from enum import Enum

class Genero(Enum):
    DRAMA = "Drama"
    COMEDIA = "Comedia"
    MUSICAL = "Musical"
    FANTASIA = "Fantasía"
    TERROR = "Terror"
    ROMANCE = "Romance"
    CIRCO = "Circo"
    EXPERIMENTAL = "Experimental"

#No funciona la importación, cuando se inicializa, la instancia Teatro no existe
#    def __init__(self, directores):
#        directores = self.getDirectores()
#        
#    def getDirectores(self):
#        from baseDatos.Teatro import Teatro
#        dirgenero = []
#        for director in Teatro.getInstancia().getDirectors():
#            if director.genero == self:
#                dirgenero.append(director)
#            return dirgenero
#
#    def anadirDirector(self, director):
#        self.directores.append(director)