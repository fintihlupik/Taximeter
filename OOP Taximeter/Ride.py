import time

class Ride:
    def __init__(self):
        self.time_waiting = 0
        self.time_moving = 0
        self.start_moving = None
        self.start_waiting = None
        self.moving_fare = 0.05
        self.waiting_fare = 0.02


    def moving(self):
        if self.start_moving is None:
            self.start_moving = time.time()
            print("The taxi is Mooooviiing!!") #log
        self.moving_time()
        self.start_moving = None

    def moving_time(self):
        input("Press Enter to stop moving ")
        move_time = time.time()-self.start_moving
        self.time_moving += move_time
        print(f"The taxi was moving for {move_time}")

    def waiting(self):
        if self.start_waiting is None:
            self.start_waiting = time.time()
            print("The taxi is waiting!!") #log
        self.waiting_time()
        self.start_waiting = None
    
    def waiting_time(self):
        input("Press Enter to stop waiting ")
        wait_time = time.time()-self.start_waiting
        self.time_waiting += wait_time
        print(f"The taxi was waiting for {wait_time}")
    
    def calculate_fare(self):
        total_fare = self.time_moving * self.moving_fare + self.time_waiting * self.waiting_fare
        print(f"Tiempo total de movimiento: {self.time_moving} segundos")
        print(f"Tiempo total de espera: {self.time_waiting} segundos")
        print(f"Tarifa total: ${total_fare:.2f}")

    


    
