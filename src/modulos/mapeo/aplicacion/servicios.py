import logging
import uuid
from datetime import datetime, timezone

from src.modulos.mapeo.dominio.entidades import ImagenMapeada
from src.modulos.mapeo.dominio.eventos import DatosAgrupadosEvento, DatosAgrupadosEventoFallido  
from src.modulos.mapeo.dominio.puertos.procesar_comando_mapeo import (
    PuertoProcesarComandoMapeo,
)
from src.modulos.mapeo.dominio.puertos.repositorios import RepositorioImagenMapeada
from src.modulos.mapeo.dominio.servicios import ServicioDominioMapeo
from src.modulos.mapeo.infraestructura.adaptadores.mapear_datos import (
    AdaptadorMapearDatos,
)
from src.modulos.mapeo.infraestructura.despachadores import DespachadorMapeo

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
        self.despachador = DespachadorMapeo()

    def procesar_comando_mapeo(
        self, id_imagen_anonimizada: uuid.UUID, id_imagen_importada: uuid.UUID, etiquetas_patologicas: list[str], ruta_imagen_anonimizada: str, evento_a_fallar:str
    ):
        id_imagen_mapeada = uuid.uuid4()
        try:
            self.servicio_dominio.validar_imagen(id_imagen_anonimizada=str(id_imagen_anonimizada))

            datos_mapeados = self.adaptador_mapeo.mapear_datos(
                str(id_imagen_anonimizada), etiquetas_patologicas, ruta_imagen_anonimizada
            )

            if not datos_mapeados:
                raise ValueError("Error: No se pudo mapear la imagen")

            imagen_mapeada = ImagenMapeada(
                id=id_imagen_mapeada,
                id_cluster_patologia=datos_mapeados["id_cluster_patologia"],
                ruta_imagen_anonimizada=datos_mapeados["ruta_imagen_anonimizada"]
            )

            self.repositorio_imagenes.agregar(imagen_mapeada)

            if evento_a_fallar == 'DatosAgrupados':
                raise ValueError("Error: Error al mapear los datos")

            evento = DatosAgrupadosEvento(
                id_imagen_importada = id_imagen_importada,
                id_imagen_anonimizada = id_imagen_anonimizada,
                id_imagen_mapeada = id_imagen_mapeada,
                cluster_id = datos_mapeados["id_cluster_patologia"],
                ruta_imagen_anonimizada = datos_mapeados["ruta_imagen_anonimizada"],
                evento_a_fallar = evento_a_fallar
            )

            self.despachador.publicar_evento(evento, "datos-agrupados")

            logger.info(
                f"👉 Imagen {id_imagen_mapeada} mapeada y evento publicado al topico datos-agrupados: {evento}"
            )

        except Exception as e:
            evento = DatosAgrupadosEventoFallido(
                id_imagen_mapeada=id_imagen_mapeada,
                id_imagen_anonimizada=id_imagen_anonimizada,
                id_imagen_importada=id_imagen_importada
            )

            self.despachador.publicar_evento_fallido(evento, 'datos-agrupados-fallido')
            logger.error(f"❌ Error al mapear la imagen y evento publicado al topico datos-agrupados-fallido: {e}")
            raise

    def procesar_comando_revertir_mapeo(self, id_imagen_mapeada: str):
        try:
            imagen_mapeada = self.repositorio_imagenes.obtener_por_id(id_imagen_mapeada)

            if imagen_mapeada:
                self.repositorio_imagenes.eliminar(imagen_mapeada.id)

                logger.info(f"🔄 Reversión ejecutada: Imagen mapeada {imagen_mapeada} eliminada.")
            else:
                logger.warning(f"⚠️ No se encontró la imagen mapeada {id_imagen_mapeada}, no hay nada que eliminar.")

        except Exception as e:
            logger.error(f"❌ Error al revertir el mapeo de datos para la imagen {id_imagen_mapeada}: {e}")
            raise