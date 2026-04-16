"""
Interfaces de repositorios del dominio.

Las interfaces de repositorios definen contratos para el acceso
a datos. Siguen el principio de Inversión de Dependencias (DIP),
donde el dominio define qué operaciones necesita y la capa de
infraestructura implementa cómo se realizan.

Esto permite:
- Cambiar implementaciones sin afectar el dominio
- Testing con mocks/stubs
- Independencia de tecnologías de persistencia
"""
