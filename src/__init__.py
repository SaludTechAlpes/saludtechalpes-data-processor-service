import os
import pulsar
import json
import logging
from flask import Flask, jsonify
from src.config import Config
from src.modulos.anonimizacion.infraestructura.despachadores import Despachador

# Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))
config = Config()

# Inicializar Pulsar
pulsar_cliente = None

def create_app(configuracion=None):
    global pulsar_cliente

    # Inicializa la aplicación Flask
    app = Flask(__name__, instance_relative_config=True)

    # Inicializar Pulsar solo una vez
    pulsar_cliente = pulsar.Client(f'pulsar://{config.PULSAR_HOST}:6650')
    despachador = Despachador()

    @app.route("/health")
    def health():
        return {
            "status": "up",
            "application_name": config.APP_NAME,
            "environment": config.ENVIRONMENT
        }

    @app.route("/test-pulsar", methods=["GET"])
    def test_pulsar():
        """
        Endpoint para probar la publicación de eventos en Pulsar.
        """
        try:
            # Crear evento de prueba
            evento_prueba = {
                "id_imagen": "123e4567-e89b-12d3-a456-426614174000",
                "ruta_imagen_anonimizada": "/ruta/fake/imagen.dcm",
                "id_paciente": "111e2222-e33b-44d5-a666-777888999000",
                "modalidad": "Rayos X",
                "region_anatomica": "Tórax",
                "fecha_estudio": "2024-02-21T12:34:56Z",
                "etiquetas_patologicas": ["Normal"]
            }

            # Publicar evento en Pulsar
            despachador.publicar_evento(evento_prueba, "eventos-anonimizacion")

            return jsonify({"message": "Evento de prueba enviado a Pulsar"}), 200
        except Exception as e:
            logger.error(f"🚨 Error al enviar evento de prueba: {e}")
            return jsonify({"error": "Error al enviar evento a Pulsar"}), 500

    # Cerrar Pulsar cuando la aplicación termina
    @app.teardown_appcontext
    def cerrar_pulsar(exception=None):
        global pulsar_cliente
        if pulsar_cliente:
            pulsar_cliente.close()
            logger.info("🔴 Cliente Pulsar cerrado al detener Flask.")

    return app
