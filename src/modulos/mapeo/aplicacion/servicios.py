import logging
import uuid
from datetime import datetime, timezone

from src.modulos.mapeo.dominio.entidades import ImagenMapeada
from src.modulos.mapeo.dominio.eventos import DatosMapeadosEvento
from src.modulos.mapeo.dominio.puertos.procesar_comando_mapeo import (
    PuertoProcesarComandoMapeo,
)
from src.modulos.mapeo.dominio.puertos.repositorios import RepositorioImagenMapeada
from src.modulos.mapeo.dominio.servicios import ServicioDominioMapeo
from src.modulos.mapeo.infraestructura.adaptadores.mapear_datos import (
    AdaptadorMapearDatos,
)
from src.modulos.mapeo.infraestructura.despachadores import Despachador

# Configurar logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ServicioAplicacionMapeo(PuertoProcesarComandoMapeo):
    def __init__(
        self,
        adaptador_mapeo: AdaptadorMapearDatos,
        repositorio_imagenes: RepositorioImagenMapeada,
    ):
        self.adaptador_mapeo = adaptador_mapeo
        self.repositorio_imagenes = repositorio_imagenes
        self.servicio_dominio = ServicioDominioMapeo()
        self.despachador = Despachador()

    def procesar_comando_mapeo(
        self, id_imagen: uuid.UUID, etiquetas_patologicas: list[str], ruta_imagen_anonimizada: str
    ):
        try:
            self.servicio_dominio.validar_imagen(id_imagen=str(id_imagen))

            datos_mapeados = self.adaptador_mapeo.mapear_datos(
                str(id_imagen), etiquetas_patologicas, ruta_imagen_anonimizada
            )

            if not datos_mapeados:
                raise ValueError("Error: No se pudo mapear la imagen")

            id_imagen_mapeada = uuid.uuid4()
            imagen_mapeada = ImagenMapeada(
                id=id_imagen_mapeada,
                imagen_mapeada_id=datos_mapeados["id_imagen"],
                id_cluster_patologia=datos_mapeados["id_cluster_patologia"],
                ruta_imagen_anonimizada=datos_mapeados["ruta_imagen_anonimizada"]
            )

            self.repositorio_imagenes.agregar(imagen_mapeada)

            evento = DatosMapeadosEvento(
                cluster_id = datos_mapeados["id_cluster_patologia"],
                ruta_imagen_anonimizada = datos_mapeados["ruta_imagen_anonimizada"],
            )

            self.despachador.publicar_evento(evento, "datos-agrupados")

            logger.info(
                f"👉 Imagen {id_imagen} mapeada y evento publicado al topico datos-agrupados: {evento}"
            )

        except Exception as e:
            logger.error(f"❌ Error al mapear la imagen: {e}")
            raise
