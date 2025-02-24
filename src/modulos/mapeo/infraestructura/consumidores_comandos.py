from src.modulos.mapeo.infraestructura.schema.v1.comandos import ComandoMapearDatos
from src.modulos.mapeo.dominio.puertos.procesar_comando_anonimizacion import PuertoProcesarComandoMapeo
from src.seedwork.infraestructura.consumidor_pulsar import ConsumidorPulsar
import pulsar
import logging

# Configuración de logs
logging.basicConfig(level=logging.DEBUG)  # Usamos DEBUG para obtener más información
logger = logging.getLogger(__name__)

class ConsumidorComandosMapeo(ConsumidorPulsar):
    """
    Consumidor de comandos de mapeo que usa Pulsar.
    """
    def __init__(self, puerto_mapeo: PuertoProcesarComandoMapeo):
        cliente = pulsar.Client('pulsar://broker:6650')
        super().__init__(cliente, "comandos-mapeo", "saludtech-sub-comandos", ComandoMapearDatos)
        self.puerto_mapeo = puerto_mapeo

    def procesar_mensaje(self, data):
        self.puerto_mapeo.procesar_comando_mapeo(
            id_imagen=data.id_imagen,
            ruta_imagen=data.ruta_imagen,
            id_paciente=data.id_paciente,
            modalidad=data.modalidad,
            region_anatomica=data.region_anatomica,
            fecha_estudio=data.fecha_estudio,
            etiquetas_patologicas=data.etiquetas_patologicas
        )
