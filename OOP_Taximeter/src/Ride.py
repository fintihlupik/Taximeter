import time
import os
import datetime
import logging
from src.Login import Login
import sqlite3

### Hace el seguimiento de un viaje en taxi: el tiempo de movimiento y espera, el cálculo del costo total y el registro del viaje en el fichero y en la base de datos.
class Ride:

    def __init__(self):
        self.time_waiting = 0
        self.time_moving = 0
        self.start_moving = None
        self.start_waiting = None
        self.moving_fare = 0.05
        self.waiting_fare = 0.02
        self.logger = logging.getLogger(self.__class__.__name__)  # Crea un logger con el nombre de Program

### Inicia o detiene el movimiento del taxi.
    def moving(self):
        if self.start_moving is None:
            self.start_moving = time.time()
            print("\033[92m🚗 The taxi is Mooooviiing!\033[0m 🚗") 
        opt = self.moving_time()
        self.start_moving = None
        print()
        #os.system('cls' if os.name == 'nt' else 'clear')
        if opt != '':
            os.system('cls' if os.name == 'nt' else 'clear')
            return 'e' 
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            return 's'      

### Calcula el tiempo que el taxi ha estado en movimiento.
    def moving_time(self):
        opt = input("Press Enter to stop moving or any key+Enter to end the trip ")
        move_time = time.time()-self.start_moving # llamo time para ver el tiempo actual
        self.time_moving += move_time
        print(f"\033[92mThe taxi was moving for {move_time:.2f} seconds\033[0m")
        time.sleep(1)
        self.logger.info(f"Taxi in movement")
        return opt

###  Inicia o detiene el estado de espera del taxi.
    def waiting(self):
        if self.start_waiting is None:
            self.start_waiting = time.time()
            print("\033[93m⏱️ The taxi is waiting!\033[0m ⏱️") # Log
        opt = self.waiting_time()
        self.start_waiting = None
        if opt != '':
            os.system('cls' if os.name == 'nt' else 'clear')
            return 'e' 
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            return 'm' 

### Calcula el tiempo que el taxi ha estado esperando.
    def waiting_time(self):
        opt = input("Press Enter to stop waiting or any key+Enter to end the trip")
        wait_time = time.time()-self.start_waiting
        self.time_waiting += wait_time
        print(f"\033[93mThe taxi was waiting for {wait_time:.2f} seconds\033[0m")
        time.sleep(1)
        self.logger.info(f"Taxi is waiting")
        return opt

### Permite al usuario actualizar las tarifas por segundo para el movimiento y la espera.
    def update_rates(self):
        upd_fares = input("\nPress 0 if you want to change the rates or Enter to use the default ones: ")
        if upd_fares == '0':
            while True:
                try:
                    self.moving_fare  = float(input("Please type the new rate when the taxi is moving: "))
                    self.waiting_fare = float(input("Please type the new rate when the taxi is stopped: "))
                    if self.moving_fare <= 0 or self.waiting_fare <= 0:
                        print("\033[91mError. Rates must be greater than 0\033[0m")
                    else:
                        break
                except ValueError:
                    print("\033[91mInvalid input. Please enter a valid number.\033[0m")
        self.logger.info(f"Rates configured: Stopped={self.waiting_fare}, Moving={self.moving_fare}")

###  Calcula el costo total del viaje basándose en los tiempos de movimiento y espera.
    def calculate_fare(self):
        moving_fare = self.time_moving * self.moving_fare
        stopped_fare = self.time_waiting * self.waiting_fare
        total_fare = stopped_fare + moving_fare
        print(f"\033[94mTotal movement time: {self.time_moving:.2f} seconds\033[0m")
        print(f"\033[94mTotal waiting time: {self.time_waiting:.2f} seconds\033[0m")
        print(f"\033[94mTotal fare: {total_fare:.2f}€\033[0m")
        self.save_trip(total_fare)
        print()
        input("Press Enter to continue ")
        os.system('cls' if os.name == 'nt' else 'clear')
        self.logger.debug(f"Trip ended. Stopped fare={stopped_fare:.2f} sec, Moving fare={moving_fare:.2f} sec, Total={total_fare:.2f}€")
    


### Registra el viaje en un archivo de texto y en la base de datos.
    def save_trip(self, total_fare):
        if not os.path.exists("persistence/history"):
            os.makedirs("persistence/history")
        history_path = f"persistence/history/{Login.username}_rides.txt"
        with open( history_path, "a", encoding="utf-8") as file:
            file.write(f"Ride on {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')} - Total fare: {total_fare:.2f} €\n")
        self.logger.info(f"Trip added to txt history")

        conexion = sqlite3.connect('persistence/taxi.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (Login.username,))
        user_id = cursor.fetchone()
        cursor.execute("INSERT INTO rides (user_id, date, total_fare) VALUES (?, ?, ?)", (user_id[0],datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'), round(total_fare,2)))
        conexion.commit()
        conexion.close()
        self.logger.info(f"Trip added to SQL history")