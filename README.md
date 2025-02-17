# Taximeter
El Taximetro digital implementa las siguientes funcionalidades básicas:
- Inicia un trayecto.
- Calcula tarifa mientras el taxi está parado.
- Calcula tarifa mientras el taxi está en movimiento.
- Finaliza un trayecto y muestra el total en euros.
- Permite iniciar un nuevo trayecto sin cerrar el programa.

A nivel de implementación utiliza:
- El enfoque orientado a objetos
- Un registro histórico de trayectos pasados en un archivo de texto plano.
- Una base de datos para almacenar los registros de trayectos pasados.
- La configuración de precios para adaptarse a la demanda actual.
- Un sistema de logs para la trazabilidad del código.
- Un sistema de autenticación con contraseñas (login) para proteger el acceso al programa.

La aplicación está dockerizada para facilitar su despliegue y portabilidad.
