import os
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_swagger import swagger
from src.config import Config

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))
config = Config()

def create_app(configuracion=None):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)

    @app.route("/health")
    def health():
        return {
            "status": "up",
            "application_name": config.APP_NAME,
            "environment": config.ENVIRONMENT
        }

    return app