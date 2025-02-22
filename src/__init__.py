import os
import pulsar
import json
import logging
import threading

from flask import Flask, jsonify
from config import Config
from modulos.ingesta.infraestructura.despachadores import Despachador
from modulos.ingesta.dominio.comandos import DatosImportadosComando
import modulos.anonimizacion.infraestructura.consumidores as anonimizacion_consumidores
from config.db import Base, engine

# Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))
config = Config()

# Inicializar Pulsar (Se usará globalmente)
pulsar_cliente = pulsar.Client('pulsar://broker:6650')

def comenzar_consumidor():
    """
    Inicia los consumidores en hilos separados.
    """
    pulsar_cliente.create_producer("comandos-ingesta")
    threading.Thread(target=anonimizacion_consumidores.suscribirse_a_comandos, daemon=True).start()

def create_app(configuracion=None):
    global pulsar_cliente

    app = Flask(__name__, instance_relative_config=True)

    with app.app_context():
        Base.metadata.create_all(engine) 
        if not app.config.get('TESTING'):
            comenzar_consumidor()

    despachador_ingesta = Despachador()

    

    @app.route("/health")
    def health():
        return {
            "status": "up",
            "application_name": config.APP_NAME,
            "environment": config.ENVIRONMENT
        }

    @app.route("/simular-ingesta-evento", methods=["GET"])
    def simular_ingesta_evento():
        """
        Endpoint para probar la publicación de comandos en Pulsar.
        """
        try:
            comando_prueba = DatosImportadosComando(
                ruta_imagen="/ruta/fake/imagen.dcm",
                ruta_metadatos="/ruta/fake/metadatos.pdf",
            )

            despachador_ingesta.publicar_comando(comando_prueba, "comandos-ingesta")

            return jsonify({"message": "Comando enviado a Pulsar"}), 200
        except Exception as e:
            logger.error(f"Error al enviar comando de prueba: {e}")
            return jsonify({"error": "Error al enviar comando a Pulsar"}), 500

    

    # Cerrar Pulsar cuando la aplicación termina
    @app.teardown_appcontext
    def cerrar_pulsar(exception=None):
        global pulsar_cliente
        if pulsar_cliente:
            pulsar_cliente.close()
            logger.info("Cliente Pulsar cerrado al detener Flask.")

    return app
