from src.application.dtos.pdf_dtos import ArchivoEntradaDTO
from src.domain.exceptions.domain_exception import ValidationException


def RestrictionVerifier(archivo_dto : ArchivoEntradaDTO):
    #Verificacion de la extendion 
    if archivo_dto.extension.lower() != "pdf" :
        #Tiramos excepcion 
        raise ValidationException("El archivo debe ser un pdf ")
