import pulsar
import logging
import traceback
import json
from modulos.anonimizacion.dominio.puertos.procesar_evento_anonimizacion import PuertoProcesarEventoAnonimizacion
from seedwork.infraestructura import utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConsumidorEventosAnonimizacion:
    def __init__(self, puerto_anonimizacion: PuertoProcesarEventoAnonimizacion):
        self.cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        self.suscripcion = "subscripcion-anonimizacion"
        self.topico_eventos = "eventos-ingesta"
        self.puerto_anonimizacion = puerto_anonimizacion

    def procesar_evento(self, evento):
        try:
            data = json.loads(evento.data())
            logger.info(f"Evento recibido: {data}")

            self.puerto_anonimizacion.procesar_evento_anonimizacion(
                id_imagen=data["id_imagen"],
                ruta_imagen=data["ruta_imagen"]
            )

            logger.info(f"Imagen procesada con éxito: {data['id_imagen']}")

        except Exception as e:
            logger.error(f"Error al procesar el evento: {e}")
            traceback.print_exc()

    def iniciar_consumidor(self):
        consumidor = self.cliente.subscribe(
            self.topico_eventos, self.suscripcion, consumer_type=pulsar.ConsumerType.Shared
        )

        while True:
            try:
                mensaje = consumidor.receive()
                self.procesar_evento(mensaje)
                consumidor.acknowledge(mensaje)
            except Exception as e:
                logger.error(f"Error en la recepción del evento: {e}")
                consumidor.negative_acknowledge(mensaje)

    def cerrar(self):
        self.cliente.close()
