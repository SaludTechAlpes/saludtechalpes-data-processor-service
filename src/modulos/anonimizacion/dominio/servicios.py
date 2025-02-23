from src.modulos.anonimizacion.dominio.reglas import FormatoImagenValido
from src.seedwork.dominio.servicios import Servicio

class ServicioDominioAnonimizacion(Servicio):
    
    def validar_imagen(self, ruta_imagen: str):
        self.validar_regla(FormatoImagenValido(ruta_imagen))