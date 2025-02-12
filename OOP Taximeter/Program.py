from Ride import Ride
import time

class Program:

    def __init__(self):
        self.current_trip = None

    def start(self):
        self.current_trip = Ride()
        print("Welcome and enjoy your trip")
        self.moving()

    def moving(self):
        if self.current_trip.start_moving is None:
            self.current_trip.start_moving = time.time()
            print("The taxi is Mooooviiing!!") #log
        self.moving_time()
        self.current_trip.start_moving = None
    
    def moving_time(self):
        input("Press Enter to stop moving ")
        move_time = time.time()-self.current_trip.start_moving
        self.current_trip.time_moving += move_time
        print(f"The taxi was moving for {move_time}")

    def waiting(self):
        if self.current_trip.start_waiting is None:
            self.current_trip.start_waiting = time.time()
            print("The taxi is waiting!!") #log
        self.waiting_time()
        self.current_trip.start_waiting = None
    
    def waiting_time(self):
        input("Press Enter to stop waiting ")
        wait_time = time.time()-self.current_trip.start_waiting
        self.current_trip.time_waiting += wait_time
        print(f"The taxi was waiting for {wait_time}")

    def welcome(self):
        print("\n***** Bienvenido al taximetro *****")
        print("Este programa te permite calcular las tarifas de un taxi.")    
    
    def main_menu(self, custom_options):
        print("\n Select an option:")
        options = {
                        't': "Start a new trip",
                        's': "Stop the taxi",
                        'm': "Move the taxi",
                        'e': "End the trip",
                        'q': "Exit",
                        'h': "History",
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
        while True:
            self.welcome()
            # si autenticar devolvio true sigo el flujo
            option = self.main_menu(["t", "s", "m", "e", "q"])
            while True:
                if option == "t":
                    self.start()
                    option = self.main_menu(["s", "e", "q"])
                if option in ['m','s','e']:
                    if self.current_trip is None:
                        print("Error. No trip in progress.") #+ log de error
                        option = self.main_menu(["t", "q"])
                    elif option == 'm':
                        self.moving()
                        option = self.main_menu(["s", "e", "q"])
                    elif option == 's':
                        self.waiting()
                        option = self.main_menu(["m", "e", "q"])
                    elif option == 'e':
                        self.current_trip.calculate_fare()
                        break
                elif option == "q":
                    exit()
            print('Fuera del primer while')
            option = self.main_menu(["t", "q"])
            if(option == 'q'):
                break
            
        
             

            


if __name__ == "__main__":
    program = Program()
    program.main()