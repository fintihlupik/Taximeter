import time
import locale
import os
import datetime
import logging

class Ride:
    def __init__(self):
        self.time_waiting = 0
        self.time_moving = 0
        self.start_moving = None
        self.start_waiting = None
        self.moving_fare = 0.05
        self.waiting_fare = 0.02
        self.logger = logging.getLogger(self.__class__.__name__)  # Crea un logger con el nombre de Program

    def moving(self):
        if self.start_moving is None:
            self.start_moving = time.time()
            print("\033[92m🚗 The taxi is Mooooviiing!\033[0m") 
        self.moving_time()
        self.start_moving = None

    def moving_time(self):
        input("Press Enter to stop moving ")
        move_time = time.time()-self.start_moving
        self.time_moving += move_time
        print(f"\033[92mThe taxi was moving for {move_time:.2f} seconds\033[0m")
        time.sleep(1.5)
        os.system('cls' if os.name == 'nt' else 'clear')
        self.logger.info(f"Taxi in movement")

    def waiting(self):
        if self.start_waiting is None:
            self.start_waiting = time.time()
            print("\033[93m⏱️ The taxi is waiting!\033[0m") # Log
        self.waiting_time()
        self.start_waiting = None
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def waiting_time(self):
        input("Press Enter to stop waiting ")
        wait_time = time.time()-self.start_waiting
        self.time_waiting += wait_time
        print(f"\033[93mThe taxi was waiting for {wait_time:.2f} seconds\033[0m")
        time.sleep(1.5)

    def update_rates(self):
        upd_fares = input("Press 0 if you want to change the rates or Enter to use the default ones: ")
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
    
    def calculate_fare(self):
        locale.setlocale(locale.LC_ALL, '')
        moving_fare = self.time_moving * self.moving_fare
        stopped_fare = self.time_waiting * self.waiting_fare
        total_fare = locale.currency(stopped_fare + moving_fare)
        print(f"Total movement time: {self.time_moving:.2f} segundos")
        print(f"Total waiting time: {self.time_waiting:.2f} segundos")
        print(f"Total fare: {total_fare}")
        self.save_trip(total_fare)
        time.sleep(2.7)
        os.system('cls' if os.name == 'nt' else 'clear')
        self.logger.debug(f"Trip ended. Stopped fare={stopped_fare:.2f} sec, Moving fare={moving_fare:.2f} sec, Total={total_fare}")

    def save_trip(self, total_fare):
            if not os.path.exists("logs"):
                os.makedirs("logs")
            with open("logs/rides_history.txt", "a", encoding="utf-8") as file:
                file.write(f"Ride on {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')} - Total fare: {total_fare}\n")
            self.logger.info(f"Trip added to history")


    


    
