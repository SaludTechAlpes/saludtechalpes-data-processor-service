from src.modulos.mapeo.dominio.reglas import ImagenExiste
from src.seedwork.dominio.servicios import Servicio

class ServicioDominioMapeo(Servicio):
    
    def validar_imagen(self, id_imagen_anonimizada: str):
        self.validar_regla(ImagenExiste(id_imagen_anonimizada))
