from src.modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoAnonimizarDatos, ComandoRevertirAnonimizacionDatos
from src.modulos.anonimizacion.dominio.puertos.procesar_comando_anonimizacion import PuertoProcesarComandoAnonimizacion
from src.seedwork.infraestructura.consumidor_pulsar import ConsumidorPulsar
from src.modulos.anonimizacion.dominio.comandos import AnonimizarDatosComando, RevertirAnonimizacionDatosComando
from src.config.config import Config
import pulsar
import logging

config = Config()

# Configuración de logs
logging.basicConfig(level=logging.DEBUG)  # Usamos DEBUG para obtener más información
logger = logging.getLogger(__name__)

class ConsumidorComandoAnonimizacion(ConsumidorPulsar):
    def __init__(self, puerto_anonimizacion: PuertoProcesarComandoAnonimizacion):
        cliente = pulsar.Client(f'pulsar://{config.BROKER_HOST}:6650')

        super().__init__(cliente, "anonimizar-datos", "saludtech-sub-comandos", ComandoAnonimizarDatos)
        self.puerto_anonimizacion = puerto_anonimizacion

    def procesar_mensaje(self, data):
        self.puerto_anonimizacion.procesar_comando_anonimizacion(
            id_imagen_importada=data.id_imagen_importada,
            ruta_imagen_importada=data.ruta_imagen_importada,
            ruta_metadatos_importados=data.ruta_metadatos_importados,
            evento_a_fallar=data.evento_a_fallar
        )
        

class ConsumidorComandoRevetirAnonimizacion(ConsumidorPulsar):
    def __init__(self, puerto_anonimizacion: PuertoProcesarComandoAnonimizacion):
        cliente = pulsar.Client(f'pulsar://{config.BROKER_HOST}:6650')

        super().__init__(cliente, "revertir-anonimizacion-datos", "saludtech-sub-comandos", ComandoRevertirAnonimizacionDatos)
        self.puerto_anonimizacion = puerto_anonimizacion

    def procesar_mensaje(self, data):
        self.puerto_anonimizacion.procesar_comando_revertir_anonimizacion(
            id_imagen_anonimizada=data.id_imagen_anonimizada,
        )