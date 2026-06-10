from src.application.dtos.pdf_dtos import ArchivoEntradaDTO
from src.domain.exceptions.domain_exception import ValidationException
from src.infrastructure.config.settings import get_settings

def restriction_verifier(archivo_dto : ArchivoEntradaDTO):
    #instanciamos configuracion
    settings=get_settings()

    #Verificacion de la extendion 
    if archivo_dto.extension.lower() != "pdf" :
        #Tiramos excepcion 
        raise ValidationException("El archivo debe ser un pdf ")
    #Verificacion de tamaño-
    if len(archivo_dto.contenido) >= settings.max_size :
        #Tiramos excepcion-
        raise ValidationException("El archivo es demasiado grande")
    #Verificacion archivo no vacio 
    if len(archivo_dto.contenido) < settings.min_size :
        #TIramos excepcion-
        raise ValidationException("El archivo esta vacio")
