"""Tests para RegistroProcesamiento."""

from src.domain.entities.registro_procesamiento import RegistroProcesamiento


class TestRegistroProcesamientoCreacion:
    """Tests para validar la creación de RegistroProcesamiento."""

    def test_registro_procesamiento_se_crea_con_campos_obligatorios(self) -> None:
        nombre_prueba = "apuntes_universidad.pdf"
        texto_prueba = "Este es el contenido extraído."

        registro = RegistroProcesamiento(
            nombre_archivo_original=nombre_prueba,
            contenido_extraido=texto_prueba,
            hash_contenido="",
        )

        assert registro.nombre_archivo_original == nombre_prueba
        assert registro.contenido_extraido == texto_prueba
        assert registro.hash_contenido == ""
        assert registro.id is not None
        assert registro.created_at is not None
        assert registro.updated_at is not None

    def test_registro_procesamiento_con_hash_valido(self) -> None:
        hash_sha256 = "a" * 64

        registro = RegistroProcesamiento(
            nombre_archivo_original="documento.pdf",
            contenido_extraido="Texto extraído.",
            hash_contenido=hash_sha256,
        )

        assert registro.hash_contenido == hash_sha256