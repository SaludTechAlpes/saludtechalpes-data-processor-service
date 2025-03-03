from src.modulos.ingesta.infraestructura.schema.v1.eventos import EventoDatosImportados
from src.seedwork.infraestructura.consumidor_pulsar import ConsumidorPulsar
from src.modulos.anonimizacion.infraestructura.despachadores import Despachador
from src.modulos.anonimizacion.dominio.comandos import AnonimizarDatosComando
import pulsar
import logging
from src.config.config import Config

config = Config()

# Configuración de logs
logging.basicConfig(level=logging.DEBUG)  # Usamos DEBUG para obtener más información
logger = logging.getLogger(__name__)

class ConsumidorEventosIngesta(ConsumidorPulsar):
    """
    Consumidor de eventos de ingesta que usa Pulsar.
    """
    despachador = Despachador()

    def __init__(self):
        cliente = pulsar.Client(f'pulsar://{config.BROKER_HOST}:6650')
        super().__init__(cliente, "datos-importados", "saludtech-sub-eventos", EventoDatosImportados)
        

    def procesar_mensaje(self, data):
        comando_anonimizar = AnonimizarDatosComando(
            ruta_imagen="/ruta/fake/imagen.dcm",
            ruta_metadatos="/ruta/fake/metadatos.pdf",
        )
        self.despachador.publicar_comando(comando_anonimizar, "anonimizar-datos")
