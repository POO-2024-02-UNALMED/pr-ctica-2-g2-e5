class Director(Artista):
    directors = []
    def __init__(nombre, id, genero):
        self.genero = genero
        self.horario = []
        super.__init__(nombre, id)
        Teatro.getInstancia().directors.append(self)
        Teatro.getInstancia().artistas.append(self)
        directors.append(self)
        genero.anadirDirector(self)
    
    def str(){
        return "Nombre: " + self.nombre + "\n" + "Identificación: " + self.id + "\n" + "Género: " + self.genero
    }
    
    def isDisponible(inicio, fin):
        for evento in horario:
            if inicio < evento[1] && fin > evento[0]:
                return False
                pass
        return True 
