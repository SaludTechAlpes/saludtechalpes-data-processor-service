from src.modulos.mapeo.infraestructura.schema.v1.eventos import EventoDatosMapeados
from src.seedwork.infraestructura.consumidor_pulsar import ConsumidorPulsar
from src.modulos.mapeo.infraestructura.despachadores import Despachador
from src.modulos.mapeo.dominio.comandos import MapearDatosComando
import pulsar
import logging

# Configuración de logs
logging.basicConfig(level=logging.DEBUG)  # Usamos DEBUG para obtener más información
logger = logging.getLogger(__name__)

class ConsumidorEventosAnonimizacion(ConsumidorPulsar):
    """
    Consumidor de eventos de anonimización que usa Pulsar.
    """
    despachador = Despachador()

    def __init__(self):
        cliente = pulsar.Client('pulsar://broker:6650')
        super().__init__(cliente, "eventos-anonimizacion", "saludtech-sub-eventos", EventoDatosMapeados)
        

    def procesar_mensaje(self, data):
        comando_mapear = MapearDatosComando(
            id_imagen=data.id_imagen,
            etiquetas_patologicas=data.etiquetas_patologicas
        )
        self.despachador.publicar_comando(comando_mapear, "comandos-mapeo")
        logger.info(f"Comando públicado al tópico comandos-mapeo: {comando_mapear}")
