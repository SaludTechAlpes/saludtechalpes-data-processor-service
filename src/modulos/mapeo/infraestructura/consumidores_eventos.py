from src.config.config import Config
from src.modulos.anonimizacion.infraestructura.schema.v1.eventos import EventoDatosAnonimizados
from src.seedwork.infraestructura.consumidor_pulsar import ConsumidorPulsar
from src.modulos.mapeo.infraestructura.despachadores import Despachador
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
    despachador = Despachador()

    def __init__(self):
        cliente = pulsar.Client(f'pulsar://{config.BROKER_HOST}:6650')
        super().__init__(cliente, "eventos-anonimizacion", "saludtech-sub-eventos", EventoDatosAnonimizados)
        

    def procesar_mensaje(self, data):
        logger.info(f"Evento de anonimización recibido: {data}")
        comando_mapear = MapearDatosComando(
            id_imagen=data.id_imagen,
            etiquetas_patologicas=data.etiquetas_patologicas,
            ruta_imagen_anonimizada=data.ruta_imagen_anonimizada
        )
        self.despachador.publicar_comando(comando_mapear, "comandos-mapeo")
        logger.info(f"Comando públicado al tópico comandos-mapeo: {comando_mapear}")
