from modulos.anonimizacion.dominio.entidades import ImagenAnonimizada, MetadatosAnonimizados
from modulos.anonimizacion.infraestructura.dto import ImagenAnonimizadaDTO, MetadatosAnonimizadosDTO
from seedwork.dominio.repositorios import Mapeador


class MapeadorImagenAnonimizada(Mapeador):
    def obtener_tipo(self) -> type:
        return ImagenAnonimizada.__class__
    
    def entidad_a_dto(self, imagen: ImagenAnonimizada) -> ImagenAnonimizadaDTO:
        metadatos_dto = None
        if imagen.metadatos:
            metadatos_dto = MetadatosAnonimizadosDTO(
                id=imagen.metadatos.id,
                token_paciente=imagen.metadatos.token_paciente,
                modalidad=imagen.metadatos.modalidad,
                region_anatomica=imagen.metadatos.region_anatomica,
                fecha_estudio=imagen.metadatos.fecha_estudio,
                etiquetas=imagen.metadatos.etiquetas  
            )

        return ImagenAnonimizadaDTO(
            id=imagen.id,
            ruta_imagen_anonimizada=imagen.ruta_imagen_anonimizada,
            fecha_procesamiento=imagen.fecha_procesamiento,
            metadatos=metadatos_dto
        )

    def dto_a_entidad(self, dto: ImagenAnonimizadaDTO) -> ImagenAnonimizada:
        metadatos_entidad = None
        if dto.metadatos:
            metadatos_entidad = MetadatosAnonimizados(
                id=dto.metadatos.id,
                token_paciente=dto.metadatos.token_paciente,
                modalidad=dto.metadatos.modalidad,
                region_anatomica=dto.metadatos.region_anatomica,
                fecha_estudio=dto.metadatos.fecha_estudio,
                etiquetas=dto.metadatos.etiquetas if dto.metadatos.etiquetas else []
            )

        return ImagenAnonimizada(
            id=dto.id,
            ruta_imagen_anonimizada=dto.ruta_imagen_anonimizada,
            fecha_procesamiento=dto.fecha_procesamiento,
            metadatos=metadatos_entidad
        )
