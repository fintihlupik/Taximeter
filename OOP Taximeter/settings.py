import sqlite3
import logging
import os

### Crea las tablas necesarias en la base de datos SQLite si no existen. También configura el registro de logs.
### Parámetros: Ninguno.
def create_tables():
    logs() #configura el registro de logs
    if not os.path.exists("persistence"):  #Verifica si existe el directorio "persistence". Si no existe, lo crea.
        os.makedirs("persistence")
    try:
        with sqlite3.connect('persistence/taxi.db') as conexion:#Establece una conexión con la base de datos SQLite ubicada en "persistence/taxi.db".
            cursor = conexion.cursor() #Cada programa o hilo debe obtener un cursor, es como una "sesión" con la base de datos(no se p acceder simultaneamente)

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS rides (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    date TEXT,
                    total_fare REAL,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')

            conexion.commit()
            logging.debug("Tables exist")
    except sqlite3.Error as e: #Captura cualquier error que ocurra durante la creación de las tablas y registra un mensaje de error con detalles del error.
        logging.error("Error creating tables")
        print(f"Error al crear tablas: {e}")

### Configura el registro de logs en un archivo llamado "taximeter.log" ubicado en el directorio "logs".
### Parámetros: Ninguno.
def logs():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    #Configura el nivel de registro a DEBUG, lo que significa que se registrarán todos los eventos desde DEBUG hasta CRITICAL.
    #Establece el formato de cada entrada de log, incluyendo la fecha, el nombre del logger, el nivel de log y el mensaje.
    logging.basicConfig(filename='logs/taximeter.log', 
        level=logging.DEBUG, # Los niveles que se van a registrar en los logs, a partir de DEBUG.
        format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s', 
        datefmt='%d-%m-%Y %H:%M:%S',
        encoding="utf-8"
    )
