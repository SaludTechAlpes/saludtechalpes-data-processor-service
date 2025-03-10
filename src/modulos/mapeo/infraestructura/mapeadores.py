from src.modulos.mapeo.dominio.entidades import ImagenMapeada
from src.modulos.mapeo.infraestructura.dto import ImagenMapeadaDTO
from src.seedwork.dominio.repositorios import Mapeador


class MapeadorImagenMapeada(Mapeador):
    def obtener_tipo(self) -> type:
        return ImagenMapeada.__class__
    
    def entidad_a_dto(self, imagen: ImagenMapeada) -> ImagenMapeadaDTO:
        return ImagenMapeadaDTO(
            id=imagen.id,
            id_cluster_patologia=imagen.id_cluster_patologia,
            ruta_imagen_anonimizada=imagen.ruta_imagen_anonimizada,
        )

    def dto_a_entidad(self, dto: ImagenMapeadaDTO) -> ImagenMapeada:
        return ImagenMapeada(
            id=dto.id,
            id_cluster_patologia=dto.id_cluster_patologia,
            ruta_imagen_anonimizada=dto.ruta_imagen_anonimizada,
        )
