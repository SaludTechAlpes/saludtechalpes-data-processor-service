import pulsar,_pulsar  
from pulsar.schema import AvroSchema
import uuid
import time
import logging
import traceback

from modulos.ingesta.infraestructura.schema.v1.comandos import ComandoAnonimizarDatos
from seedwork.infraestructura import utils


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def suscribirse_a_comandos():
    cliente = None
    try:
        cliente = pulsar.Client('pulsar://broker:6650')
        consumidor = cliente.subscribe('comandos-ingesta', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='saludtech-sub-comandos', schema=AvroSchema(ComandoAnonimizarDatos))

        while True:
            mensaje = consumidor.receive()
            logger.info(f'Comando recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except Exception as error:
        logging.error(f'Error suscribiendose al tópico de comandos: {error}')
        traceback.print_exc()
        if cliente:
            cliente.close()