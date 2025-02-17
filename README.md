# Taximeter

## Acerca del proyecto
El Taximetro digital es un proyecto en Python que implementa las siguientes funcionalidades básicas:
- Iniciar un trayecto.
- Calcular tarifa mientras el taxi está parado.
- Calcular tarifa mientras el taxi está en movimiento.
- Finalizar un trayecto y muestra el total en euros.
- Permitir iniciar un nuevo trayecto sin cerrar el programa.
- 
## Implementación
A nivel de implementación utiliza:
- El enfoque orientado a objetos
- Un registro histórico de trayectos pasados en un archivo de texto plano.
- Una base de datos para almacenar los registros de trayectos pasados.
- La configuración de precios para adaptarse a la demanda actual.
- Un sistema de logs para la trazabilidad del código.
- Un sistema de autenticación con contraseñas (login) para proteger el acceso al programa.

## Despliegue
La aplicación está dockerizada para facilitar su despliegue y portabilidad.

Pasos a seguir en el terminal para su ejecución (asegurate de tener Docker corriendo):

1. Clonar el repositorio
   
   `git clone https://github.com/fintihlupik/Taximeter.git taximeter`
   
3. Acceder a la carpeta
   
   `cd taximeter`
   
4. Construir la imagen
   
  `docker build -t taximeterfintihlupik .`
  
5. Crear y ejecutar un nuevo contenedor a partir de la imagen
   
   `docker run -it taximeterfintihlupik`

