from abc import ABC, abstractmethod
from datetime import datetime


class Flight(ABC):
    def __init__(self, flight_number, destination, ticket_price, capacity):
        self.flight_number = flight_number
        self.destination = destination
        self.ticket_price = ticket_price
        self.capacity = capacity
        self.booked_seats = 0

    @abstractmethod
    def get_flight_type(self):
        pass

    def is_available(self):
        return self.booked_seats < self.capacity


class DomesticFlight(Flight):
    def get_flight_type(self):
        return "Belföldi"


class InternationalFlight(Flight):
    def get_flight_type(self):
        return "Nemzetközi"


class Airline:
    def __init__(self, name):
        self.name = name
        self.flights = []

    def add_flight(self, flight):
        self.flights.append(flight)

    def find_flight(self, flight_number):
        for flight in self.flights:
            if flight.flight_number == flight_number:
                return flight
        return None


class TicketReservation:
    def __init__(self, reservation_id, flight, passenger_name, date):
        self.reservation_id = reservation_id
        self.flight = flight
        self.passenger_name = passenger_name
        self.date = date
        self.price = flight.ticket_price

    def __str__(self):
        return (f"Foglalás ID: {self.reservation_id}, Járatszám: {self.flight.flight_number}, "
                f"Cél: {self.flight.destination}, Utas: {self.passenger_name}, "
                f"Dátum: {self.date}, Ár: {self.price} Ft")


class ReservationSystem:
    def __init__(self, airline):
        self.airline = airline
        self.reservations = []
        self.reservation_counter = 1

    def reserve_ticket(self, flight_number, passenger_name, date_str):
        flight = self.airline.find_flight(flight_number)
        if not flight:
            return None, "A járat nem található!"
        if not flight.is_available():
            return None, "A járat már megtelt!"
        try:
            reservation_date = datetime.strptime(date_str, "%Y-%m-%d")
            if reservation_date.date() < datetime.now().date():
                return None, "Érvénytelen dátum!"
        except ValueError:
            return None, "Hibás dátum formátum! Használj ÉÉÉÉ-HH-NN formátumot."

        reservation_id = self.reservation_counter
        self.reservation_counter += 1
        new_reservation = TicketReservation(reservation_id, flight, passenger_name, date_str)
        self.reservations.append(new_reservation)
        flight.booked_seats += 1
        return new_reservation.price, "Sikeres foglalás!"

    def cancel_reservation(self, reservation_id):
        for reservation in self.reservations:
            if reservation.reservation_id == reservation_id:
                reservation.flight.booked_seats -= 1
                self.reservations.remove(reservation)
                return True, "Foglalás törölve!"
        return False, "Foglalás nem található!"

    def list_reservations(self):
        return self.reservations.copy()


def initialize_system():
    airline = Airline("Magyar Repülő")

    flights = [
        DomesticFlight("D123", "Budapest", 15000, 2),
        DomesticFlight("D456", "Debrecen", 10000, 100),
        InternationalFlight("I789", "London", 50000, 3)
    ]

    for flight in flights:
        airline.add_flight(flight)

    reservation_system = ReservationSystem(airline)

    # Előre betöltött foglalások
    reservations = [
        ("D123", "Kiss János", "2024-06-01"),
        ("D123", "Nagy Éva", "2024-06-01"),
        ("I789", "Smith John", "2024-07-15"),
        ("I789", "Kovács Anna", "2024-07-15"),
        ("I789", "Szabó Péter", "2024-07-15"),
        ("D456", "Tóth Eszter", "2024-08-20")
    ]

    for flight_num, name, date in reservations:
        reservation_system.reserve_ticket(flight_num, name, date)

    return reservation_system


def main():
    system = initialize_system()
    print("Üdvözöljük a repülőjegy foglalási rendszerben!")

    while True:
        print("\nVálassz műveletet:")
        print("1. Jegyfoglalás")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("4. Kilépés")
        choice = input("Választásod: ")

        if choice == "1":
            print("\nElérhető járatok:")
            for flight in system.airline.flights:
                status = "Szabad helyek: {}".format(
                    flight.capacity - flight.booked_seats) if flight.is_available() else "Megetelt"
                print(
                    f"{flight.flight_number} - {flight.destination} ({flight.get_flight_type()}), Ár: {flight.ticket_price} Ft, Státusz: {status}")

            flight_num = input("Járatszám: ")
            name = input("Utas neve: ")
            date = input("Dátum (ÉÉÉÉ-HH-NN): ")

            price, msg = system.reserve_ticket(flight_num, name, date)
            print(msg)
            if price:
                print(f"Fizetendő összeg: {price} Ft")

        elif choice == "2":
            res_id = input("Foglalási ID: ")
            try:
                success, msg = system.cancel_reservation(int(res_id))
                print(msg)
            except ValueError:
                print("Érvénytelen ID formátum!")

        elif choice == "3":
            reservations = system.list_reservations()
            if reservations:
                print("\nÖsszes foglalás:")
                for res in reservations:
                    print(res)
            else:
                print("Nincsenek foglalások")

        elif choice == "4":
            print("Viszlát!")
            break

        else:
            print("Érvénytelen választás!")


if __name__ == "__main__":
    main()