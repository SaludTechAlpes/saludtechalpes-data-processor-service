from abc import ABC, abstractmethod

class PuertoAnonimizarDatos(ABC):
    @abstractmethod
    def anonimizar_datos(self, ruta_imagen_importada: str, ruta_metadatos_importados: str) -> dict:
        ...