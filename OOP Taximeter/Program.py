from Ride import Ride
import time

# Rates, con round y euro y Control de errores!!!!
# history (y poner un if en menus) y logs y os clear

class Program:

    def __init__(self):
        self.current_trip = None

    def start(self):
        print("Welcome on board!")
        print("The default fare while the taxi is stopped is 2 cents per second.") 
        print("The default fare while the taxi is moving is 5 cents per second.") 
        self.current_trip = Ride()
        upd_fares = input("Press 0 if you want to change the rates or Enter to use the default ones: ")
        if upd_fares == '0':
            while True:
                try:
                    self.current_trip.moving_fare  = float(input("Please type the new rate when the taxi is moving: "))
                    self.current_trip.waiting_fare = float(input("Please type the new rate when the taxi is stopped: "))
                    if self.current_trip.moving_fare <= 0 or self.current_trip.waiting_fare <= 0:
                        print("Error. Rates must be greater than 0")
                    else:
                        break
                except ValueError:
                    print("Invalid input. Please enter a valid number.") 

    def welcome(self):
        print("\n***** Welcome to the digital taximeter *****")
        print("This program allows you to calculate taxi fares.")          
    
    def main_menu(self, custom_options):
        print("\n Select an option:")
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
        return option

    def main(self):
        # si autenticar devolvio true sigo el flujo
        history = False
        while True:
            if history != True:
                self.welcome()
                option = self.main_menu(["t", "q"])
            while True:
                if option == 't':
                    self.start()
                    option = self.main_menu(["s", "e", "q"])
                elif option == 'm':
                    self.current_trip.moving()
                    option = self.main_menu(["s", "e", "q"])
                elif option == 's':
                    self.current_trip.waiting()
                    option = self.main_menu(["m", "e", "q"])
                elif option == 'e':
                    self.current_trip.calculate_fare()
                    break
                elif option == 'h':
                    print("Mostrar historico")
                    break #temporal
                elif option == 'q':
                    exit()
            history = True
            option = self.main_menu(['t', 'h', 'q'])
            if option == 'q':
                break

if __name__ == "__main__":
    program = Program()
    program.main()