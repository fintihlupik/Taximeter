import time

def welcome():
    print("\n***** Bienvenido al taximetro *****")
    print(" Este programa te permite calcular las tarifas de un taxi.")

def start():
    print("\n***** Inicio del trayecto. Bienvenido al bordo *****")
    return{"time_waiting":0, "time_moving":0}
    
def moving_time_to_trip(trip):
    input("Presiona Enter para parar ")
    time_moving = time.time()-trip['moving_start']
    trip['time_moving'] += time_moving
    print(f"Tiempo en movimiento:  {time_moving:.2f} segundos")
    return trip

def waiting_time_to_trip(trip):
    input("Presiona Enter para empezar el movimiento o terminar el viaje ")
    time_waiting = time.time() - trip['waiting_start']
    trip['time_waiting'] += time_waiting
    print(f"Tiempo parado:  {time_waiting:.2f} segundos")
    return trip

def to_pay(trip):
    moving_rate = float(input("Define la tarifa en movimiento: "))
    waiting_rate = float(input("Define la tarifa con taxi parado: "))
    receipt = trip['time_waiting'] * waiting_rate + trip['time_moving'] * moving_rate
    print(f"Son {receipt:.2f} euros a pagar")
    
def taximeter():
    welcome()
    while True:
        trip = start()
        while True:
            print("\nOpciones:")
            print("1. Taxi en movimiento")
            print("2. Taxi parado")
            print("3. Finalizar trayecto")
            option = input("Opcion elegida: ")
            if (option == '1'):
                print('\n')
                print("Taxi en movimiento, VAAA-MOOOO-SSS !!")
                if "moving_start" not in trip:
                    trip['moving_start'] = time.time()
                    trip = moving_time_to_trip(trip)
                    del trip["moving_start"]
            elif (option == '2'):
                print('\n')
                print("Taxi parado. Paciencia.")
                if "waiting_start" not in trip:
                    trip['waiting_start'] = time.time()
                    trip = waiting_time_to_trip(trip)
                    del trip['waiting_start']
            elif (option == '3'):
                to_pay(trip)
                break
            else:
                print('Opción no válida. Elige entre las disponibles.')
        new_trip = input("¿Deseas realizar otro viaje? (s/n) ")
        if(new_trip.lower() != 's'):
            print('Gracias por viajar con nosotros. Adiós!')
            break       
taximeter()
