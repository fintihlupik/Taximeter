#-*- coding: utf-8 -*-
from Ride import Ride
import os
import time
import logging

# y logs 
# autenticacion
# dependencias y requierements
# emojis y colorines


if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(filename='logs/taximeter.log',
    level=logging.DEBUG, # Establece los niveles que se registrarán de mensajes, nivel DEBUG y superiores.
    format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s', # Establece el formato de los mensajes de log
    datefmt='%d-%m-%Y %H:%M:%S',
    encoding="utf-8"
)

class Program:

    def __init__(self):
        self.current_trip = None
        self.logger = logging.getLogger(self.__class__.__name__)  # Crea un logger con el nombre de Program

    def start(self):
        print("Welcome on board!")
        print("The default fare while the taxi is stopped is 2 cents per second.") 
        print("The default fare while the taxi is moving is 5 cents per second.") 
        self.current_trip = Ride()
        self.current_trip.update_rates()
        self.logger.info("Ride starts")
        print ("Enjoy the trip!")
        time.sleep(0.7)
        os.system('cls' if os.name == 'nt' else 'clear')
        self.current_trip.moving()

    def welcome(self):
        print("\n***** Welcome to the digital taximeter *****")
        print("This program allows you to calculate taxi fares.")          
    
    def menu(self, custom_options):
        print("Select an option:")
        options = {
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

        option = input("Choose an option: ")
        while option not in custom_options:
            print(f"Invalid option {option}")
            option = input("Choose an option: ")
            self.logger.warning(f"Invalid input")
        os.system('cls' if os.name == 'nt' else 'clear')
        return option
    
    def view_history(self):
        os.system('cls' if os.name == 'nt' else 'clear')      
        history_path = os.path.abspath("logs/rides_history.txt")
        os.startfile(history_path) # para abrirlo con el editor del texto predeterminado del sistema
        self.logger.info(f"Showing the history")
        os.system('cls' if os.name == 'nt' else 'clear')

    def main(self):
        # si autenticar devolvio true sigo el flujo
        history = False
        while True:
            if history != True:
                self.welcome()
                option = self.menu(["t", "q"])
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
                    break #temporal
                elif option == 'q':
                    print("Goodbye")
                    time.sleep(0.5)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.logger.info(f"Exiting the system")
                    exit()
            history = True
            option = self.menu(['t', 'h', 'q'])
            if option == 'q':
                print("Goodbye")
                time.sleep(0.5)
                os.system('cls' if os.name == 'nt' else 'clear')
                self.logger.info(f"Exiting the system")
                break

if __name__ == "__main__":
    program = Program()
    program.main()