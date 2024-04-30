#%%
import random
import string
import pandas as pd
from wsgiref.handlers import format_date_time
from faker import Faker
from database import Database
import datetime
import cx_Oracle
fake = Faker()

class Database:
    def __init__(self):
        self.user = 'kenny2'
        self.password = '077790'
        self.dsn = 'XE'

    def connect(self):
        try:
            connection = cx_Oracle.connect(user=self.user, password=self.password, dsn=self.dsn)
            print("Connected to Oracle database.")
            return connection
        except cx_Oracle.Error as e:
            print(f"Error connecting to database: {e}")
            return None

class DatabaseManager:
    connection = None

    @classmethod
    def set_connection(cls, conn):
        cls.connection = conn

    @classmethod
    def get_connection(cls):
        return cls.connection
    
class Customer:
    def __init__(self):
        self.username = self.generate_username()
        self.email = self.generate_email()

    @staticmethod
    def generate_username():
        return fake.bothify(text='????###')

    @staticmethod
    def generate_name():
        return fake.name()

    @staticmethod
    def generate_identification_id():
        digits = ''.join(random.choices('0123456789', k=10))
        position = random.randint(1, 9)
        identification_id = digits[:position] + '-' + digits[position:]
        return identification_id

    @staticmethod
    def generate_email():
        domain = fake.random_element(elements=('gmail.com', 'yahoo.com', 'outlook.com'))
        max_username_length = 25 - len(domain) - 1
        username = fake.user_name()[:max_username_length]
        return f"{username}@{domain}"

    @staticmethod
    def generate_membership_id():
        return f"AAS{random.randint(10000, 99999)}"

    @staticmethod
    def generate_country():
        return fake.country()[:25]

    @staticmethod
    def generate_phone():
        remaining_digits = ''.join(random.choices('0123456789', k=9))
        phone_number = "+60" + remaining_digits
        return phone_number

    def insert_customer(login_id, cust_name, identification_id, phone, email, membership_id, country):
        connection = DatabaseManager.get_connection()
        cursor = connection.cursor()
        try:
            for i in range(len(login_id)):
                cursor.execute("""
                    INSERT INTO Customer (Login_ID, Cust_Name, Identification_id, Phone, Email, Membership_Id, Country)
                    VALUES (:1, :2, :3, :4, :5, :6, :7)
                """, (login_id[i], cust_name[i], identification_id[i], phone[i], email[i], membership_id[i], country[i]))
            connection.commit()
            # print("Customer inserted successfully.")
        except Exception as e:
            print(f"Error inserting customers: {e}")
        finally:
            cursor.close()


class Booking:

    def __init__(self, username, booking_details):
        self.username = username
        self.booking_details = booking_details
        self.connection = self.get_connection()  # Get database connection

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

    def insert_booking(book_no, login_id, flight_no, seat_id, book_time, boarding_datetime, departure_airport, arrival_airport):
        cursor = DatabaseManager.connection.cursor()
        try:
            for i in range(len(book_no)):
                cursor.execute("""
                    INSERT INTO Booking (Book_No, Login_ID, Flight_No, Seat_id, Book_Time, Boarding_Datetime, Departure_Airport, Arrival_Airport)
                    VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
                """, (book_no[i], login_id[i], flight_no[i], seat_id[i], book_time[i], boarding_datetime[i], departure_airport[i], arrival_airport[i]))
            DatabaseManager.connection.commit()
            # print("Bookings inserted successfully.")
        except Exception as e:
            print(f"Error inserting bookings: {e}")
        finally:
            cursor.close()


# %%
