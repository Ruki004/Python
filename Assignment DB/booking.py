from wsgiref.handlers import format_date_time
from faker import Faker
import datetime

fake = Faker()

class Booking:
    def __init__(self, connection):
        self.connection = connection
    
    @staticmethod
    def rand_datetime_generator(): 
        end_date = datetime.date.today()  # Current date
        start_date = end_date - datetime.timedelta(days=90)  # 90 days ago
        random_date = fake.date_between(start_date=start_date, end_date=end_date)
        random_time = fake.time_object()
        return datetime.datetime.combine(random_date, random_time)
    
    @staticmethod
    def rand_time_no_seconds():
        # Generate a random time without seconds
        hour = fake.random_int(min=0, max=23)
        minute = fake.random_int(min=0, max=59)
        return datetime.time(hour=hour, minute=minute)
    
    @staticmethod
    def Airport_MY():
        international_airports = [
            "John F. Kennedy I.A (JFK)",
            "Los Angeles I.A (LAX)",
            "Heathrow Airport (LHR)",
            "Tokyo Haneda Airport (HND)",
            "Beijing Capital I.A(PEK)",
            "Dubai I.A (DXB)"
        ]
        malaysian_airports = [
            "Kuala Lumpur I.A (KUL)",
            "Penang I.A (PEN)",
            "Langkawi I.A (LGK)",
            "Kuching I.A (KCH)",
            "Kota Kinabalu I.A (BKI)"
        ]
        depart = fake.random_element(elements=malaysian_airports)
        arrival_options = international_airports + malaysian_airports
        arrival_options.remove(depart)
        arrival = fake.random_element(elements=arrival_options)
        return depart, arrival
    
    @staticmethod
    def rand_seat_generator():
        random_letter = fake.random_element(elements=[chr(i) for i in range(65, 91)])
        numeric_part = fake.numerify(text='##')
        seat = f"{random_letter}{numeric_part}"
        return seat
    
    def insert_booking(self, book_no, login_id, flight_no, seat_id, book_time, boarding_datetime, departure_airport, arrival_airport):
        cursor = self.connection.cursor()
        try:
            # Check if all input lists have the same length
            input_lists = [book_no, login_id, flight_no, seat_id, book_time, boarding_datetime, departure_airport, arrival_airport]
            list_lengths = [len(lst) for lst in input_lists]
            if len(set(list_lengths)) != 1:
                raise ValueError("All input lists must have the same length.")

            # Iterate over the input lists and execute the SQL query
            for i in range(len(book_no)):
                cursor.execute("""
                    INSERT INTO Booking (Book_No, Login_ID, Flight_No, Seat_id, Book_Time, Boarding_Datetime, Departure_Airport, Arrival_Airport)
                    VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
                """, (book_no[i], login_id[i], flight_no[i], seat_id[i], book_time[i], boarding_datetime[i], departure_airport[i], arrival_airport[i]))
            self.connection.commit()
            print("Bookings inserted successfully.")
        except Exception as e:
            print(f"Error inserting bookings: {e}")
        finally:
            cursor.close()
