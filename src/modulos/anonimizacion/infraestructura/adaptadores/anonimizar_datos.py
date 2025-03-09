from src.modulos.anonimizacion.dominio.puertos.anonimizar_datos import PuertoAnonimizarDatos
import random
from datetime import datetime, timezone
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class AdaptadorAnonimizarDatos(PuertoAnonimizarDatos):
    MODALIDADES_PERMITIDAS = ["Rayos X", "Resonancia Magnética", "Tomografía Computarizada", "Ultrasonido", "Mamografía"]
    REGIONES_ANATOMICAS = ["Tórax", "Cerebro", "Abdomen", "Rodilla", "Columna Vertebral"]
    ETIQUETAS_PATOLOGICAS = ["Normal", "Fractura", "Tumor", "Infección", "Inflamación", "Maligno", "Benigno"]

    def anonimizar_datos(self, ruta_imagen_importada: str, ruta_metadatos_importados: str) -> dict:
        ruta_anonimizada = self._anonimizar_imagen(ruta_imagen_importada)
        metadatos_extraidos = self._extraccion_metadatos(ruta_metadatos_importados)

        logger.info(f"👉 Datos anonimizados de manera exitosa. Ruta imagen anonimizada {ruta_anonimizada} y ruta metadatos anonimizados {metadatos_extraidos}")

        return {
            "ruta_imagen_anonimizada": ruta_anonimizada,
            "metadatos_anonimizados": metadatos_extraidos
        }
    
    def _anonimizar_imagen(self, ruta_imagen_importada) -> str:
        return "ruta_imagen_anonimizada"

    def _extraccion_metadatos(self, ruta_metadatos_importados) -> dict:
        metadatos_simulados = {
            "modalidad": random.choice(self.MODALIDADES_PERMITIDAS),
            "region_anatomica": random.choice(self.REGIONES_ANATOMICAS),
            "fecha_estudio": datetime.now(timezone.utc),
            "etiquetas": self._generar_etiquetas_aleatorias()
        }
        return metadatos_simulados

    def _generar_etiquetas_aleatorias(self) -> list:
        num_etiquetas = random.randint(1, 3)
        return random.sample(self.ETIQUETAS_PATOLOGICAS, num_etiquetas)
