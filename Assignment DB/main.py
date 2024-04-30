#%%
from debugpy import connect
from sympy import print_fcode
from booking import Booking
from connect import DB
from cust import Customer
from cgitb import text
from multiprocessing import connection
from matplotlib.pylab import f
import pandas as pd
from faker import Faker
import datetime
import random

# Generate fake data
fake = Faker()

# Modify Customer_data function to accept customer_login_ids as a parameter
def Customer_data(cust_data):
    login_id = [(Customer.generate_login_id() in range(cust_data))]  # Use customer_login_ids directly
    missing_logins = cust_data - len(login_id)
    login_id.extend([Customer.generate_login_id() for _ in range(missing_logins)])  # Generate additional login IDs if needed
    password = [Customer.generate_password() for _ in range(cust_data)]
    cust_name = [Customer.generate_name() for _ in range(cust_data)]
    identification_id = [Customer.generate_identification_id() for _ in range(cust_data)]
    phone = [Customer.generate_phone() for _ in range(cust_data)]
    email = [Customer.generate_email() for _ in range(cust_data)]
    membership_id = [Customer.generate_membership_id() for _ in range(cust_data)]
    country = [Customer.generate_country() for _ in range(cust_data)]

    return login_id, password, cust_name, identification_id, phone, email, membership_id, country

# Modify Booking_data function to accept customer_login_ids as a parameter
def Booking_data(book_data, customer_login_ids):
    book_no = []
    login_id = []
    flight_no = []
    seat_id = [] 
    book_time = []
    boarding_datetime = []
    departure_airport = []
    arrival_airport = []

    book_no = [fake.numerify(text='MY######') for _ in range(book_data)]
    login_id = customer_login_ids  # Use customer_login_ids directly
    flight_no = [fake.random_uppercase_letter() + fake.random_uppercase_letter() + fake.numerify(text='####') for _ in range(book_data)]
    seat_id = [Booking.rand_seat_generator() for _ in range(book_data)]
    book_time = [Booking.rand_datetime_generator() for _ in range(book_data)]  # Use rand_datetime_generator
    boarding_datetime = [datetime.datetime.combine(fake.date_time_between(start_date=bt.date(), end_date=bt.date() + datetime.timedelta(days=90)), Booking.rand_time_no_seconds()) for bt in book_time]  # Use rand_time_no_seconds
    for _ in range(book_data):
        departure, arrival = Booking.Airport_MY()
        departure_airport.append(departure)
        arrival_airport.append(arrival)

    return book_no, login_id, flight_no, seat_id, book_time, boarding_datetime, departure_airport, arrival_airport

database = DB()
connection = database.connect()

if connection:
    try:
        # Generate fake customer data
        cust_data = 3
        book_data = 10

        # Generate login IDs for customers
        login_id = [Customer.generate_login_id() for _ in range(cust_data)]

        # Generate other customer data
        password = [Customer.generate_password() for _ in range(cust_data)]
        cust_name = [Customer.generate_name() for _ in range(cust_data)]
        identification_id = [Customer.generate_identification_id() for _ in range(cust_data)]
        phone = [Customer.generate_phone() for _ in range(cust_data)]
        email= [Customer.generate_email() for _ in range(cust_data)]
        membership_id = [Customer.generate_membership_id() for _ in range(cust_data)]
        country = [Customer.generate_country() for _ in range(cust_data)]

        login_id, password, cust_name, identification_id, phone, email, membership_id, country=Customer_data(cust_data)

        # Create a Customer instance and insert customers
        customer = Customer(connection)
        customer.insert_customer(login_id, password, cust_name, identification_id, phone, email, membership_id, country)

        # # Retrieve existing login IDs from the Customer table
        existing_login_id = []# Retrieve existing login IDs from the database

        # # Use existing login IDs for bookings
        booking_login_id= existing_login_id[:cust_data]
        
        # login_ids = [customer.generate_login_id() for _ in range(cust_data)]

        # Generate booking data
        book_no, login_id, flight_no, seat_id, book_time, boarding_datetime, departure_airport, arrival_airport = Booking_data(book_data,booking_login_id)

        # Debug: Print lengths of all input lists
        print("Length of book_no:", len(book_no))
        print("Length of login_id:", len(login_id))
        print("Length of flight_no:", len(flight_no))
        print("Length of seat_id:", len(seat_id))
        print("Length of book_time:", len(book_time))
        print("Length of boarding_datetime:", len(boarding_datetime))
        print("Length of departure_airport:", len(departure_airport))
        print("Length of arrival_airport:", len(arrival_airport))

        # Create a Booking instance and insert bookings
        booking = Booking(connection)
        booking.insert_booking(book_no, login_id, flight_no, seat_id, book_time, boarding_datetime, departure_airport, arrival_airport)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close connection
        connection.close()
else:
    print("Unable to connect to the database.")







# %%
