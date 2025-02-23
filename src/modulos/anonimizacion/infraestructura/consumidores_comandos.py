from modulos.ingesta.infraestructura.schema.v1.comandos import ComandoAnonimizarDatos
from modulos.anonimizacion.dominio.puertos.procesar_comando_anonimizacion import PuertoProcesarComandoAnonimizacion
from seedwork.infraestructura.consumidor_pulsar import ConsumidorPulsar
import pulsar
import logging

# Configuración de logs
logging.basicConfig(level=logging.DEBUG)  # Usamos DEBUG para obtener más información
logger = logging.getLogger(__name__)

class ConsumidorComandosAnonimizacion(ConsumidorPulsar):
    """
    Consumidor de comandos de anonimización que usa Pulsar.
    """
    def __init__(self, puerto_anonimizacion: PuertoProcesarComandoAnonimizacion):
        cliente = pulsar.Client('pulsar://broker:6650')
        super().__init__(cliente, "comandos-anonimizacion", "saludtech-sub-comandos", ComandoAnonimizarDatos)
        self.puerto_anonimizacion = puerto_anonimizacion

    def procesar_mensaje(self, data):
        self.puerto_anonimizacion.procesar_comando_anonimizacion(
            ruta_imagen=data.ruta_imagen,
            ruta_metadatos=data.ruta_metadatos
        )
