import sqlite3
import logging
import os

def create_tables():
    logs()
    if not os.path.exists("persistence"):
        os.makedirs("persistence")
    try:
        with sqlite3.connect('persistence/taxi.db') as conexion:
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
    except sqlite3.Error as e:
        logging.error("Error creating tables")
        print(f"Error al crear tablas: {e}")

def logs():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logging.basicConfig(filename='logs/taximeter.log',
        level=logging.DEBUG, # Los niveles que se van a registrar en los logs, a partir de DEBUG.
        format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s', 
        datefmt='%d-%m-%Y %H:%M:%S',
        encoding="utf-8"
    )
