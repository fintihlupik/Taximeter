from Ride import Ride
import os
import time
import logging
from settings import create_tables
from Login import Login
import sqlite3

### Esta clase maneja la lógica principal del programa, incluyendo el menú, la autenticación y el inicio de viajes.
class Program:

    def __init__(self):
        self.current_trip = None
        self.logger = logging.getLogger(self.__class__.__name__)  # Crea un logger con el nombre de Program
        self.login = Login()

### Inicia un nuevo viaje en taxi.
    def start(self):
        print("\033[95m🚕 Welcome on board!\033[0m")
        print("Default fare while stopped: 2 cents/sec")
        print("Default fare while moving: 5 cents/sec") 
        self.current_trip = Ride()
        self.current_trip.update_rates()
        self.logger.info("Ride starts")
        print("\033[95mEnjoy the trip!\033[0m")
        time.sleep(0.7)
        os.system('cls' if os.name == 'nt' else 'clear')
        self.current_trip.moving() # El viaje comienza en movimiento

### Muestra un mensaje de bienvenida al programa.
    def welcome(self):
        print("***** 🚕 Digital Taximeter *****")
        print("Calculate taxi fares easily\n")          

### Descripción: Muestra un menú con opciones personalizadas y devuelve la opción seleccionada por el usuario.
### Parámetros: custom_options: Lista de opciones que se deben mostrar en el menú.
    def menu(self, custom_options):
        print("Select an option: ")
        options = {
                        '1': "Log in",
                        '2': "Sign up",
                        't': "Start a new trip",
                        's': "Stop the taxi",
                        'm': "Move the taxi",
                        'e': "End the trip",
                        'h': "Show the history",
                        'q': "Exit",
                    }
        for opt in options:
            if opt in custom_options:
                print(f"{opt}: {options[opt]}")

        option = input("\nChoose an option: ")
        while option not in custom_options:
            print("\033[91mInvalid option. Please choose again.\033[0m")
            option = input("Choose an option: ")
            self.logger.warning(f"Invalid input")
        os.system('cls' if os.name == 'nt' else 'clear')
        return option
    
### Muestra el historial de viajes del usuario actual.
    def view_history(self):
        os.system('cls' if os.name == 'nt' else 'clear')      
        history_path = os.path.abspath("logs/rides_history.txt")
        os.startfile(history_path) # para abrirlo con el editor del texto predeterminado del sistema
        rides,conexion = self.fetch_history()
        self.print_sql_history(rides,conexion)
        input("\nPress Enter to continue ")
        os.system('cls' if os.name == 'nt' else 'clear')

### Obtiene el historial de viajes del usuario actual desde la base de datos.
    def fetch_history(self):
        try:
            conexion = sqlite3.connect('persistence/taxi.db')
            cursor = conexion.cursor()
            cursor.execute("""
                                SELECT r.date, r.total_fare 
                                FROM rides r 
                                JOIN users u ON r.user_id = u.id 
                                WHERE u.username = ?
                            """, (Login.username,))
            rides = cursor.fetchall()
            return rides, conexion
        except Exception as e:
            print(f"Error al obtener el historial: {e}")
            return [], None
        finally:
            if conexion is not None:
                conexion.close()

### Muestra el historial de viajes obtenido desde la base de datos
    def print_sql_history(self,rides,conexion):
        for ride in rides:
            print(f"Date: {ride[0]}, Total Fare: {ride[1]} €")
        conexion.close()

### Muestra un mensaje de despedida y cierra el programa.
    def goodbye(self):
        print("\033[95mGoodbye\033[0m")
        time.sleep(0.7)
        os.system('cls' if os.name == 'nt' else 'clear')
        self.logger.info(f"Exiting the system")
        exit()

### Maneja la autenticación del usuario según la opción seleccionada.
    def authenticate(self,option):
        if option == "1":
            self.login.login_user()
        elif option == "2":
            self.login.register_user()
        elif option == "q":
            self.goodbye()

### Método principal que ejecuta la lógica del programa.
    def main(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.welcome()
        option = self.menu(["1", "2", "q"])
        self.authenticate(option)
        option = None
        history,con = self.fetch_history()
        #print(f" SELF HISTORY !!!  {history}")
        while True:
            if not history:
                self.welcome()
                option = self.menu(["t", "q"])
            elif not option:
                option = self.menu(["t", "h" ,"q"])
            while True:
                if option == 't':
                    self.start()
                    option = self.menu(["s", "e", "q"])
                elif option == 'm':
                    self.current_trip.moving()
                    option = self.menu(["s", "e", "q"])
                elif option == 's':
                    self.current_trip.waiting()
                    option = self.menu(["m", "e", "q"])
                elif option == 'e':
                    self.current_trip.calculate_fare()
                    break
                elif option == 'h':
                    self.view_history()
                    break
                elif option == 'q':
                    self.goodbye()
            history = True
            option = self.menu(['t', 'h', 'q'])
            if option == 'q':
                self.goodbye()

if __name__ == "__main__":
    program = Program()
    create_tables()
    program.main()



