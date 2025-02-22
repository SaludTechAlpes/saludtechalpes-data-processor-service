from modulos.anonimizacion.dominio.reglas import FormatoImagenValido
from seedwork.dominio.servicios import Servicio

class ServicioDominioAnonimizacion(Servicio):
    
    def validar_imagen(self, ruta_imagen: str):
        self.validar_regla(FormatoImagenValido(ruta_imagen))