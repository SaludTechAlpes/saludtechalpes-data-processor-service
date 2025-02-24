from src.modulos.anonimizacion.infraestructura.schema.v1.eventos import EventoDatosAnonimizados
from src.seedwork.infraestructura.consumidor_pulsar import ConsumidorPulsar
from src.modulos.mapeo.infraestructura.despachadores import Despachador
from src.modulos.mapeo.dominio.comandos import MapearDatosComando
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
        super().__init__(cliente, "eventos-ingesta", "saludtech-sub-eventos", EventoDatosAnonimizados)
        

    def procesar_mensaje(self, data):
        comando_mapear = MapearDatosComando(
            id_imagen="fakeIdImage",
            ruta_imagen_anonimizada="/ruta/fake/imagen.dcm",
            id_paciente="fakeIdPatient",
            modalidad="Rayos X",
            region_anatomica="Tórax",
            fecha_estudio="2021-01-01T00:00:00",
            etiquetas_patologicas=["fakePathologicalLabels"]  
        )
        self.despachador.publicar_comando(comando_mapear, "comandos-mapeo")
        logger.info(f"Comando públicado al tópico comandos-mapeo: {comando_mapear}")
