from abc import ABC, abstractmethod

class PuertoAnonimizarDatos(ABC):
    @abstractmethod
    def anonimizar_datos(self, ruta_imagen: str, ruta_metadatos: str) -> dict:
        ...