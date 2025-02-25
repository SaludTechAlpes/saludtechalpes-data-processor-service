import logging
import random
from datetime import datetime, timezone

from src.modulos.mapeo.dominio.puertos.mapear_datos import PuertoMapearDatos

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdaptadorMapearDatos(PuertoMapearDatos):
    def mapear_datos(self, id_imagen: str, etiquetas_patologicas: list[str]) -> dict:
        imagen_mapeada = self._mapear_imagen(id_imagen, etiquetas_patologicas)

        logger.info("Imagen mapeada de manera exitosa")

        return imagen_mapeada

    def _mapear_imagen(self, id_imagen: str, etiquetas_patologicas: list[str]) -> dict:
        return {
            "id_imagen": id_imagen,
            "id_cluster_patologia": self._generar_id_cluster_patologia(etiquetas_patologicas),
        }

    def _generar_id_cluster_patologia(self, etiquetas_patologicas: list[str]) -> str:
        return etiquetas_patologicas[0]
