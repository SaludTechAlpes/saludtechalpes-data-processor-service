from src.modulos.ingesta.infraestructura.schema.v1.comandos import ComandoAnonimizarDatos
from src.modulos.anonimizacion.dominio.puertos.procesar_comando_anonimizacion import PuertoProcesarComandoAnonimizacion
from src.seedwork.infraestructura.consumidor_pulsar import ConsumidorPulsar
from src.config.config import Config
import pulsar
import logging

config = Config()

# Configuración de logs
logging.basicConfig(level=logging.DEBUG)  # Usamos DEBUG para obtener más información
logger = logging.getLogger(__name__)

class ConsumidorComandosAnonimizacion(ConsumidorPulsar):
    """
    Consumidor de comandos de anonimización que usa Pulsar.
    """
    def __init__(self, puerto_anonimizacion: PuertoProcesarComandoAnonimizacion):
        cliente = pulsar.Client(f'pulsar://{config.BROKER_HOST}:6650')
        super().__init__(cliente, "anonimizar-datos", "saludtech-sub-comandos", ComandoAnonimizarDatos)
        self.puerto_anonimizacion = puerto_anonimizacion

    def procesar_mensaje(self, data):
        self.puerto_anonimizacion.procesar_comando_anonimizacion(
            ruta_imagen=data.ruta_imagen,
            ruta_metadatos=data.ruta_metadatos
        )
