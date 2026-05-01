from io import BytesIO

from src.application.dtos.pdf_dtos import ArchivoSalidaDTO, TextoExtraidoDTO


class GenerarArchivoTxtUseCase:
    def execute(self, dto: TextoExtraidoDTO, nombre_original: str) -> ArchivoSalidaDTO:
        nombre_sin_extension = (
            nombre_original.rsplit(".", 1)[0]
            if "." in nombre_original
            else nombre_original
        )
        nombre_txt = f"{nombre_sin_extension}.txt"

        buffer = BytesIO()
        buffer.write(dto.contenido.encode("utf-8"))
        buffer.seek(0)

        return ArchivoSalidaDTO(
            nombre=nombre_txt, buffer=buffer, content_type="text/plain; charset=utf-8"
        )
