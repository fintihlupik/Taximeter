import sqlite3
import hashlib
import getpass
import time
import os
import logging

### Esta clase maneja el registro y el inicio de sesión de usuarios en una aplicación.
class Login:

    username = None #Variable de clase que almacena el nombre de usuario del usuario logueado.

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)  # Crea un logger con el nombre de la clase
        Login.username = None

### Descripción: Registra un nuevo usuario en la base de datos.
### Parámetros: Ninguno.
    def register_user(self):
        username = input("Enter your username: ")

        conexion = sqlite3.connect('persistence/taxi.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            print("\033[91mUsername already exists. Please choose another one.\033[0m")
            self.logger.warning(f"Existing username")
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear') #  Limpia la pantalla y redirige al usuario al inicio de sesión.
            return self.register_user()

        password = getpass.getpass("Enter your password: ")
        confirm_password = getpass.getpass("Confirm your password: ")
        
        if password != confirm_password:
            print("\033[91mPasswords do not match. Please try again.\033[0m")
            self.logger.warning(f"Passwords do not match")
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            return self.register_user()
        
        hashed_password = self.hash_password(password)
        
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))  # Almacena el hash
        conexion.commit()
        conexion.close()
        
        print("\033[92mUser registered successfully.\033[0m")
        self.logger.info(f"User registered successfully.")
        print("Please log in")
        time.sleep(1.2)
        os.system('cls' if os.name == 'nt' else 'clear')
        self.login_user()
    
### Descripción: Inicia sesión con un usuario existente.
### Parámetros: attempts=3: Número de intentos permitidos para el inicio de sesión. Por defecto, son 3 intentos.
    def login_user(self, attempts=3):
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")

        hashed_password = self.hash_password(password)  # Hash la contraseña ingresada
        
        with sqlite3.connect('persistence/taxi.db') as conexion:
            cursor = conexion.cursor()
            
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
            
            if cursor.fetchone():
                Login.username = username  # Establece el usuario logueado = username
                print("\033[92mLogin successful.\033[0m")
                self.logger.debug(f"Login successful")
                time.sleep(1)
                os.system('cls' if os.name == 'nt' else 'clear')
                return True
            else:
                print("\033[91mInvalid username or password.\033[0m")
                print(f"{attempts - 1} attempts left.")
                time.sleep(1)
                if attempts > 1:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.login_user(attempts - 1)
                else:
                    print("\033[91mMaximum attempts reached. Login failed.\033[0m")
                    time.sleep(1)
                    self.logger.error(f"Incorrect username or password")
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.goodbye()
                    time.sleep(1)

### Descripción: Hashea una contraseña usando SHA-256.
### Parámetros: password: Contraseña a hashear 
    def hash_password(self,password):
        return hashlib.sha256(password.encode()).hexdigest()

### Descripción: Muestra un mensaje de despedida y cierra la aplicación.
### Parámetros: Ninguno.
    def goodbye(self):
        print("\033[95mGoodbye\033[0m")
        time.sleep(0.7)
        os.system('cls' if os.name == 'nt' else 'clear')
        self.logger.info(f"Exiting the system")
        exit()