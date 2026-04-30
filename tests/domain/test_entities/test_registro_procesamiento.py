from src.domain.entities.registro_procesamiento import RegistroProcesamiento

def test_registro_procesamiento_se_crea_con_campos_obligatorios():
    nombre_prueba = "apuntes_universidad.pdf"
    texto_prueba = "Este es el contenido extraído."

    registro = RegistroProcesamiento(
        nombre_archivo_original=nombre_prueba,
        contenido_extraido=texto_prueba
    )

    assert registro.nombre_archivo_original == nombre_prueba
    assert registro.contenido_extraido == texto_prueba
    assert registro.id is not None
    assert registro.created_at is not None
    assert registro.updated_at is not None