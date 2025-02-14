from Ride import Ride
import os
import time
import logging
from settings import create_tables
from Login import Login

# autenticacion
# dependencias y requierements
# emojis y colorines

class Program:

    def __init__(self):
        self.current_trip = None
        self.logger = logging.getLogger(self.__class__.__name__)  # Crea un logger con el nombre de Program
        self.login = Login()

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
        self.current_trip.moving()

    def welcome(self):
        print("\n***** 🚕 Digital Taximeter *****")
        print("Calculate taxi fares easily")          
    
    def menu(self, custom_options):
        print("Select an option:")
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

        option = input("Choose an option: ")
        while option not in custom_options:
            print("\033[91mInvalid option. Please choose again.\033[0m")
            option = input("Choose an option: ")
            self.logger.warning(f"Invalid input")
        os.system('cls' if os.name == 'nt' else 'clear')
        return option
    
    def view_history(self):
        os.system('cls' if os.name == 'nt' else 'clear')      
        history_path = os.path.abspath("logs/rides_history.txt")
        os.startfile(history_path) # para abrirlo con el editor del texto predeterminado del sistema
        self.logger.info(f"Showing the history")
        time.sleep(3)
        os.system('cls' if os.name == 'nt' else 'clear')

    def goodbye(self):
        print("\033[95mGoodbye\033[0m")
        time.sleep(0.7)
        os.system('cls' if os.name == 'nt' else 'clear')
        self.logger.info(f"Exiting the system")
        exit()

    def authenticate(self,option):
            if option == "1":
                self.login.login_user()
            elif option == "2":
                self.login.register_user()
            elif option == "q":
                self.goodbye()

    def main(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.welcome()
        option = self.menu(["1", "2", "q"])
        self.authenticate(option)
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
                    self.goodbye()
            history = True
            option = self.menu(['t', 'h', 'q'])
            if option == 'q':
                self.goodbye()

if __name__ == "__main__":
    program = Program()
    create_tables()
    program.main()



