from enum import Enum

class Suscripcion(Enum):
    
    BASICA = "Basica"
    PREMIUM = "Premium"
    ELITE = "Elite"
    VIP = "Vip"

# Ejemplo de uso
print(Suscripcion.BASICA)       # Suscripcion.BASICA
print(Suscripcion.BASICA.value) # "Basica"
