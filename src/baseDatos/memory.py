from Teatro import Teatro
from src.gestorAplicacion.gestionVentas.Cliente import Cliente
#arreglar importaciones

def resetMemory():
    Teatro.setInstancia( Teatro() )

if __name__ == "__main__":
    resetMemory()

    objs = [

    Cliente(id = 426, tipo= "Empresa"),
    # añadir todos los objetos de prueba acá

    print("Base de datos reinicializada")

]