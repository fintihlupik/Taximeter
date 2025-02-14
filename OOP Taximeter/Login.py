import sqlite3
import hashlib
import getpass
import time
import os
import logging
#from login_utils import failure

class Login:

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)  # Crea un logger con el nombre de Program

    def register_user(self):
        username = input("Enter your username: ")

        conexion = sqlite3.connect('taxi.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            print("\033[91mUsername already exists. Please choose another one.\033[0m")
            self.logger.warning(f"Existing username")
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
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
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
    
                    
    def login_user(self, attempts=3):
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")

        hashed_password = self.hash_password(password)  # Hash la contraseña ingresada
        
        with sqlite3.connect('taxi.db') as conexion:
            cursor = conexion.cursor()
            
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
            
            if cursor.fetchone():
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
            
    def hash_password(self,password):
        return hashlib.sha256(password.encode()).hexdigest()

    def goodbye(self):
        print("\033[95mGoodbye\033[0m")
        time.sleep(0.7)
        os.system('cls' if os.name == 'nt' else 'clear')
        self.logger.info(f"Exiting the system")
        exit()