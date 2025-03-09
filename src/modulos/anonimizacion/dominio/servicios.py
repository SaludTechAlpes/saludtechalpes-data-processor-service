from src.modulos.anonimizacion.dominio.reglas import FormatoImagenValido
from src.seedwork.dominio.servicios import Servicio

class ServicioDominioAnonimizacion(Servicio):
    
    def validar_imagen(self, id_imagen_importada: str):
        self.validar_regla(FormatoImagenValido(id_imagen_importada))