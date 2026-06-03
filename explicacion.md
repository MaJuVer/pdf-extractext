# Workflow del Proyecto: Extractor de Texto PDF

A continuación se detalla el flujo de trabajo de la aplicación, integrando las especificaciones del requerimiento de la cátedra con tu lógica de procesamiento. Todo el diseño de este flujo debe estar orientado a cumplir con la Arquitectura de Aplicaciones Empresariales y mantener un código limpio aplicando los principios SOLID, DRY, KISS y YAGNI.

## Flujo de Trabajo Principal

1. **Recepción del Archivo (Upload):**
El cliente realiza una petición a la API (desarrollada con FastAPI ) enviando un archivo, que debe ser un documento en formato PDF. Es vital que la recepción se maneje en memoria, ya que el documento no debe ser persistido temporalmente en el disco del servidor durante ninguna parte de su procesamiento.


2. **Validación de Requisitos:**
El sistema valida estrictamente el archivo entrante, verificando que su formato sea efectivamente PDF y que su peso no exceda el límite de tamaño establecido. Si la validación falla, se corta el flujo y se devuelve un error al cliente.


3. **Cálculo de Checksum y Verificación de Duplicados:**
Se calcula el checksum (suma de verificación) del archivo recibido. Con este hash, se consulta la base de datos no relacional para asegurar que el documento no exista duplicado.


* **Ruta A (El archivo ya existe):** Si el checksum coincide con un registro, se omite el procesamiento del PDF y se recupera directamente el texto que ya estaba guardado en la base de datos.
* 
**Ruta B (El archivo no existe):** Si es un documento nuevo, se procede a extraer solamente el texto de su contenido. Inmediatamente, se persiste este nuevo texto extraído junto con su checksum correspondiente en la base de datos no relacional.




4. **Generación del Archivo de Salida:**
Con el texto listo y en memoria (ya sea recuperado en la Ruta A o extraído en la Ruta B), el sistema empaqueta esta información y genera dinámicamente un nuevo archivo de texto (`.txt`).
5. **Entrega al Cliente (Download):**
La aplicación devuelve el archivo `.txt` generado como respuesta a la petición original, permitiendo que el cliente lo descargue.

## Consideraciones Técnicas Transversales

* 
**Operaciones CRUD:** De forma paralela a este flujo principal, el sistema debe proveer endpoints para realizar el CRUD completo de los documentos que ya han sido persistidos.


* 
**Gestión y Metodología:** El ciclo de vida de este desarrollo debe estar guiado estrictamente por la metodología TDD (Test-Driven Development). Además, se debe utilizar `uv` como gestor de paquetes de Python.


* 
**Infraestructura:** La configuración de la API y sus dependencias debe alinearse con la metodología 12 Factor App.
