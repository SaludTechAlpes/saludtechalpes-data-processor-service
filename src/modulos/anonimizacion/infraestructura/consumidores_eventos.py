from modulos.ingesta.infraestructura.schema.v1.eventos import EventoDatosImportados
from seedwork.infraestructura.consumidor_pulsar import ConsumidorPulsar
from modulos.anonimizacion.infraestructura.despachadores import Despachador
from modulos.anonimizacion.dominio.comandos import AnonimizarDatosComando
import pulsar
import logging

# Configuración de logs
logging.basicConfig(level=logging.DEBUG)  # Usamos DEBUG para obtener más información
logger = logging.getLogger(__name__)

class ConsumidorEventosIngesta(ConsumidorPulsar):
    """
    Consumidor de eventos de ingesta que usa Pulsar.
    """
    despachador = Despachador()

    def __init__(self):
        cliente = pulsar.Client('pulsar://broker:6650')
        super().__init__(cliente, "eventos-ingesta", "saludtech-sub-eventos", EventoDatosImportados)
        

    def procesar_mensaje(self, data):
        comando_anonimizar = AnonimizarDatosComando(
            ruta_imagen="/ruta/fake/imagen.dcm",
            ruta_metadatos="/ruta/fake/metadatos.pdf",
        )
        self.despachador.publicar_comando(comando_anonimizar, "comandos-anonimizacion")
        logger.info(f"Comando públicado al tópico comandos-anonimizacion: {comando_anonimizar}")
