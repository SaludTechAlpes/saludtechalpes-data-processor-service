from abc import ABC, abstractmethod
from uuid import UUID

class PuertoProcesarComandoAnonimizacion(ABC):
    @abstractmethod
    def procesar_comando_anonimizacion(self, ruta_imagen_importada: str, ruta_metadatos_importados: str):
        ...
    
    @abstractmethod
    def procesar_comando_anonimizacion_fallido(self, id_imagen_anonimizada: str):
        ...
