import logging

import pulsar

from src.config.config import Config
from src.modulos.mapeo.dominio.puertos.procesar_comando_mapeo import \
    PuertoProcesarComandoMapeo
from src.modulos.mapeo.infraestructura.schema.v1.comandos import \
    ComandoMapearDatos, ComandoRevertirMapeoDatos
from src.seedwork.infraestructura.consumidor_pulsar import ConsumidorPulsar

# Configuración de logs
logging.basicConfig(level=logging.DEBUG)  # Usamos DEBUG para obtener más información
logger = logging.getLogger(__name__)

config = Config()

class ConsumidorComandosMapeo(ConsumidorPulsar):
    """
    Consumidor de comandos de mapeo que usa Pulsar.
    """

    def __init__(self, puerto_mapeo: PuertoProcesarComandoMapeo):
        cliente = pulsar.Client(f'pulsar://{config.BROKER_HOST}:6650')
        super().__init__(
            cliente, "mapear-datos", "saludtech-sub-comandos", ComandoMapearDatos
        )
        self.puerto_mapeo = puerto_mapeo

    def procesar_mensaje(self, data):
        self.puerto_mapeo.procesar_comando_mapeo(
            id_imagen_anonimizada=data.id_imagen_anonimizada,
            id_imagen_importada=data.id_imagen_importada,
            etiquetas_patologicas=data.etiquetas_patologicas,
            ruta_imagen_anonimizada=data.ruta_imagen_anonimizada,
            evento_a_fallar=data.evento_a_fallar
        )

class ConsumidorComandoRevetirMapeo(ConsumidorPulsar):
    def __init__(self, puerto_mapeo: PuertoProcesarComandoMapeo):
        cliente = pulsar.Client(f'pulsar://{config.BROKER_HOST}:6650')

        super().__init__(cliente, "revertir-mapeo-datos", "saludtech-sub-comandos", ComandoRevertirMapeoDatos)
        self.puerto_mapeo = puerto_mapeo

    def procesar_mensaje(self, data):
        self.puerto_mapeo.procesar_comando_revertir_mapeo(
            id_imagen_mapeada=data.id_imagen_mapeada,
        )