from src.modulos.anonimizacion.dominio.puertos.anonimizar_datos import PuertoAnonimizarDatos
import random
from datetime import datetime, timedelta

class AdaptadorAnonimizarDatos(PuertoAnonimizarDatos):
    MODALIDADES_PERMITIDAS = ["Rayos X", "Resonancia Magnética", "Tomografía Computarizada", "Ultrasonido", "Mamografía"]
    REGIONES_ANATOMICAS = ["Tórax", "Cerebro", "Abdomen", "Rodilla", "Columna Vertebral"]
    ETIQUETAS_PATOLOGICAS = ["Normal", "Fractura", "Tumor", "Infección", "Inflamación", "Maligno", "Benigno"]

    def anonimizar_datos(self, ruta_imagen: str, ruta_archivo_metadatos: str) -> dict:
        ruta_anonimizada = self._anonimizar_imagen(ruta_imagen)
        metadatos_extraidos = self._extraccion_metadatos(ruta_archivo_metadatos)

        return {
            "ruta_imagen_anonimizada": ruta_anonimizada,
            "metadatos_anonimizados": metadatos_extraidos
        }
    
    def _anonimizar_imagen(self, ruta_imagen) -> str:
        return "ruta_imagen_anonimizada"

    def _extraccion_metadatos(self, ruta_archivo_metadatos) -> dict:
        metadatos_simulados = {
            "modalidad": random.choice(self.MODALIDADES_PERMITIDAS),
            "region_anatomica": random.choice(self.REGIONES_ANATOMICAS),
            "fecha_estudio": self._generar_fecha_aleatoria(),
            "etiquetas": self._generar_etiquetas_aleatorias()
        }
        return metadatos_simulados

    def _generar_fecha_aleatoria(self) -> str:
        dias_atras = random.randint(1, 365)
        fecha_aleatoria = datetime.now() - timedelta(days=dias_atras)
        return fecha_aleatoria.strftime("%Y-%m-%d")

    def _generar_etiquetas_aleatorias(self) -> list:
        num_etiquetas = random.randint(1, 3)
        return random.sample(self.ETIQUETAS_PATOLOGICAS, num_etiquetas)
