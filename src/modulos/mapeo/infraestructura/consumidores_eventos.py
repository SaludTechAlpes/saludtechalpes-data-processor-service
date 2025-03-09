from src.config.config import Config
from src.modulos.anonimizacion.infraestructura.schema.v1.eventos import EventoDatosAnonimizados
from src.seedwork.infraestructura.consumidor_pulsar import ConsumidorPulsar
from src.modulos.mapeo.infraestructura.despachadores import DespachadorMapeo
from src.modulos.mapeo.dominio.comandos import MapearDatosComando
import pulsar
import logging

# Configuración de logs
logging.basicConfig(level=logging.DEBUG)  # Usamos DEBUG para obtener más información
logger = logging.getLogger(__name__)

config = Config()

class ConsumidorEventosAnonimizacion(ConsumidorPulsar):
    """
    Consumidor de eventos de anonimización que usa Pulsar.
    """
    despachador = DespachadorMapeo()

    def __init__(self):
        cliente = pulsar.Client(f'pulsar://{config.BROKER_HOST}:6650')
        super().__init__(cliente, "datos-anonimizados", "saludtech-sub-eventos", EventoDatosAnonimizados)
        

    def procesar_mensaje(self, data):
        comando_mapear = MapearDatosComando(
            id_imagen_importada=data.id_imagen_importada,
            id_imagen_anonimizada=data.id_imagen_anonimizada,
            etiquetas_patologicas=data.etiquetas_patologicas,
            ruta_imagen_anonimizada=data.ruta_imagen_anonimizada,
            evento_a_fallar=data.evento_a_fallar,
        )
        self.despachador.publicar_comando(comando_mapear, "mapear-datos")
