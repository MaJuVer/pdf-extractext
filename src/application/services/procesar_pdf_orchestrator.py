"""
Orquestador para el procesamiento completo de archivos PDF.

Coordina el flujo de negocio:
1. Validar restricciones del archivo
2. Verificar magic bytes de PDF
3. Calcular hash SHA256
4. Si existe duplicado: recuperar texto de cache
5. Si es nuevo: extraer texto y guardar registro
6. Generar archivo .txt de salida
"""


from src.application.dtos.pdf_dtos import (
    ArchivoEntradaDTO,
    ProcesarPdfOutputDTO,
    TextoExtraidoDTO,
)
from src.application.interfaces.pdf_extractor_interface import PDFExtractorInterface
from src.application.services.extraer_texto import ExtraerTexto
from src.application.services.generar_archivo_txt import GenerarArchivoTxtUseCase
from src.application.services.guardar_registro_service import GuardarRegistroService
from src.application.services.pdf_validator import RestrictionVerifier
from src.domain.entities.documento_pdf import DocumentoPDF
from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.domain.exceptions.pdf_exceptions import PDFInvalidException
from src.domain.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoRepository,
)


class ProcesarPdfOrchestrator:
    """
    Orquestador que coordina el flujo completo de procesamiento de PDF.

    Este servicio aplica el patron Facade/Orchestrator para encapsular
    toda la logica de negocio en una unica operacion cohesiva.

    Responsibilities:
        - Validar entrada (extension, tamano, magic bytes)
        - Detectar duplicados por hash SHA256
        - Extraer texto o recuperar de cache
        - Persistir registro de procesamiento
        - Generar archivo .txt de salida

    Example:
        >>> orchestrator = ProcesarPdfOrchestrator(
        ...     extractor=PyPDFExtractor(),
        ...     repository=RegistroProcesamientoMongoRepositoryImpl(db)
        ... )
        >>> resultado = orchestrator.execute(archivo_dto)
        >>> # resultado.fue_cacheado indica si vino de cache
    """

    PDF_MAGIC_BYTES = b"%PDF-"

    def __init__(
        self,
        extractor: PDFExtractorInterface,
        repository: RegistroProcesamientoRepository,
    ) -> None:
        self._extractor = extractor
        self._repository = repository
        self._extraer_texto_service = ExtraerTexto(extractor)
        self._guardar_registro_service = GuardarRegistroService(repository)
        self._generar_txt_use_case = GenerarArchivoTxtUseCase()

    def execute(
        self, archivo_dto: ArchivoEntradaDTO
    ) -> ProcesarPdfOutputDTO:
        """
        Ejecuta el flujo completo de procesamiento de PDF.

        Args:
            archivo_dto: DTO con el archivo de entrada.

        Returns:
            ProcesarPdfOutputDTO con el archivo generado y metadatos.

        Raises:
            ValidationException: Si el archivo no cumple restricciones basicas.
            PDFInvalidException: Si el contenido no es un PDF valido.
            DocumentoSinTextoException: Si el PDF no contiene texto.
            DocumentoDuplicadoException: Si el hash ya existe (edge case).
        """
        RestrictionVerifier(archivo_dto)

        self._validar_magic_bytes(archivo_dto.contenido, archivo_dto.nombre)

        documento = self._crear_documento_pdf(archivo_dto)

        hash_contenido = documento.calcular_hash_sha256()

        registro_existente = self._repository.get_by_hash(hash_contenido)

        if registro_existente is not None:
            return self._procesar_ruta_cacheado(registro_existente, documento.nombre_archivo)

        return self._procesar_ruta_nuevo(documento)

    def _validar_magic_bytes(self, contenido: bytes, nombre_archivo: str) -> None:
        """
        Valida que el contenido corresponda a un PDF valido.

        Args:
            contenido: Bytes del archivo.
            nombre_archivo: Nombre del archivo para mensajes de error.

        Raises:
            PDFInvalidException: Si los magic bytes no corresponden a PDF.
        """
        if not contenido.startswith(self.PDF_MAGIC_BYTES):
            raise PDFInvalidException(nombre_archivo)

    def _crear_documento_pdf(self, archivo_dto: ArchivoEntradaDTO) -> DocumentoPDF:
        """
        Crea una entidad DocumentoPDF a partir del DTO de entrada.

        Args:
            archivo_dto: DTO con datos del archivo.

        Returns:
            Entidad DocumentoPDF validada.
        """
        return DocumentoPDF(
            nombre_archivo=archivo_dto.nombre,
            peso_bytes=len(archivo_dto.contenido),
            contenido_binario=archivo_dto.contenido,
        )

    def _procesar_ruta_cacheado(
        self, registro_existente: RegistroProcesamiento, nombre_archivo: str
    ) -> ProcesarPdfOutputDTO:
        """
        Procesa un documento duplicado usando el cache.

        Args:
            registro_existente: Registro previamente guardado.
            nombre_archivo: Nombre del archivo original.

        Returns:
            ProcesarPdfOutputDTO con datos cacheados.
        """
        contenido = registro_existente.contenido_extraido

        texto_dto = TextoExtraidoDTO(
            contenido=contenido,
            cantidad_caracteres=len(contenido),
            cantidad_palabras=len(contenido.split()),
        )

        archivo_salida = self._generar_txt_use_case.execute(texto_dto, nombre_archivo)

        return ProcesarPdfOutputDTO(
            archivo_salida=archivo_salida,
            registro=None,
            fue_cacheado=True,
        )

    def _procesar_ruta_nuevo(self, documento: DocumentoPDF) -> ProcesarPdfOutputDTO:
        """
        Procesa un documento nuevo: extrae texto, guarda y genera archivo.

        Args:
            documento: Entidad DocumentoPDF a procesar.

        Returns:
            ProcesarPdfOutputDTO con datos del nuevo procesamiento.
        """
        texto_dto = self._extraer_texto_service.execute(documento)

        registro_dto = self._guardar_registro_service.ejecutar(documento, texto_dto)

        archivo_salida = self._generar_txt_use_case.execute(
            texto_dto, documento.nombre_archivo
        )

        return ProcesarPdfOutputDTO(
            archivo_salida=archivo_salida,
            registro=registro_dto,
            fue_cacheado=False,
        )