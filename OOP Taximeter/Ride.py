
class Ride:
    def __init__(self):
        self.time_waiting = 0
        self.time_moving = 0
        self.start_moving = None
        self.start_waiting = None
        self.moving_fare = 0.05
        self.waiting_fare = 0.02
    
    def calculate_fare(self):
        total_fare = self.time_moving * self.moving_fare + self.time_waiting * self.waiting_fare
        print(f"Tiempo total de movimiento: {self.time_moving} segundos")
        print(f"Tiempo total de espera: {self.time_waiting} segundos")
        print(f"Tarifa total: ${total_fare:.2f}")

    


    
