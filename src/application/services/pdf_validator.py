from src.application.dtos.pdf_dtos import ArchivoEntradaDTO
from src.domain.exceptions.domain_exception import ValidationException

def verificar_restricciones(archivo_dto : ArchivoEntradaDTO,max_size: int,min_size: int)-> None:

    
    if archivo_dto.extension.lower() != "pdf" :
        raise ValidationException("El archivo debe ser un pdf ")
    
    if len(archivo_dto.contenido) >= max_size :
        raise ValidationException("El archivo es demasiado grande")
     
    if len(archivo_dto.contenido) < min_size :
        raise ValidationException("El archivo esta vacio")
