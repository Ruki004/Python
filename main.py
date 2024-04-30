#%%
from multiprocessing import connection
from os import name
import faker
from cust_book import Booking, Customer,DatabaseManager,Database
# from database import Database
from faker import Faker
import datetime
import pandas as pd
import random
from IPython.display import display


fake = Faker()

# Generate customer data
def Customer_data(cust_data):
    login_id = []
    cust_name = []
    identification_id = []
    phone = []
    email = []
    membership_id = []
    country = []

    for _ in range(cust_data):
        username = Customer.generate_username()  # Generate a unique username for each customer
        login_id.append(username)
        cust_name.append(Customer.generate_name())
        identification_id.append(Customer.generate_identification_id())
        phone.append(Customer.generate_phone())
        email.append(Customer.generate_email())
        membership_id.append(Customer.generate_phone())
        country.append(Customer.generate_country())

    return login_id, cust_name, identification_id, phone, email, membership_id, country

# Create DataFrame for customers
cust_data = 15
login_id, cust_name, identification_id, phone, email, membership_id, country = Customer_data(cust_data)

df_customers = pd.DataFrame({
    'Login_Id': login_id, 
    'Cust_Name': cust_name,
    'Identification_Id': identification_id,
    'Phone': phone, 
    'Email': email, 
    'Membership_Id': membership_id, 
    'Country': country
})

# Generate booking data
def Booking_data(book_data, login_ids):
    book_no = []
    flight_no = []
    seat_id = [] 
    book_time = []
    boarding_datetime = []
    departure_airport = []
    arrival_airport = []

    # Generate booking details
    for _ in range(book_data):
        book_no.append(fake.numerify(text='MY######'))
        flight_no.append(fake.random_uppercase_letter() + fake.random_uppercase_letter() + fake.numerify(text='####'))
        seat_id.append(Booking.rand_seat_generator())
        book_time.append(Booking.rand_datetime_generator())
        boarding_datetime.append(Booking.rand_datetime_generator())
        departure, arrival = Booking.Airport_MY()
        departure_airport.append(departure)
        arrival_airport.append(arrival)

    # Assign login IDs to bookings
    bookings_login_id = random.choices(login_ids, k=book_data)

    return book_no,bookings_login_id,flight_no, seat_id, book_time, boarding_datetime, departure_airport, arrival_airport

# Create DataFrame for bookings
book_data = 80 # Change value here
book_no, bookings_login_id, flight_no, seat_id, book_time, boarding_datetime, departure_airport, arrival_airport = Booking_data(book_data, login_id)

df_bookings = pd.DataFrame({
    'Book_No': book_no,
    'Login_ID': bookings_login_id,
    'Flight_No': flight_no,
    'Seat_Id': seat_id,
    'Book_Time': book_time,
    'Boarding_Datetime': boarding_datetime,
    'Departure_Airport': departure_airport,
    'Arrival_Airport': arrival_airport
})

display(df_customers)
display(df_bookings)


# Insert data into the database
# print(df_customers)
# print(df_bookings)

# print("Length of book_no:", len(book_no))
# print("Length of login_id:", len(login_id))
# print("Length of flight_no:", len(flight_no))
# print("Length of seat_id:", len(seat_id))
# print("Length of book_time:", len(book_time))
# print("Length of boarding_datetime:", len(boarding_datetime))
# print("Length of departure_airport:", len(departure_airport))
# print("Length of arrival_airport:", len(arrival_airport))

# print("Length of login_id:", len(book_no))
# print("Length of cust_name :", len(cust_name))
# print("Length of identification_Id:", len(identification_id))
# print("Length of phone:", len(phone))
# print("Length of email:", len(email))
# print("Length of membership_id:", len(membership_id))

db = Database()
# Establish the database connection
connection = db.connect()

# Set the connection in the DatabaseManager
DatabaseManager.set_connection(connection)

# Now, you can insert customer and booking data
#debug
try:
    # print("Length of login_id:", len(login_id))
    # print("Length of cust_name:", len(cust_name))
    # Print lengths of other lists as well

    Customer.insert_customer(
        login_id, 
        cust_name, 
        identification_id, 
        phone, 
        email,
        membership_id,
        country
    )
    print("Customer data inserted successfully:",cust_data)

    # print("Length of book_no:", len(book_no))
    # print("Length of login_id:", len(bookings_login_id))
    # Print lengths of other booking lists as well
    Booking.insert_booking(
        book_no, 
        bookings_login_id, 
        flight_no, 
        seat_id, 
        book_time, 
        boarding_datetime, 
        departure_airport, 
        arrival_airport
    )
    print("Booking data inserted successfully:",book_data)
except Exception as e:
    print(f"Error inserting data: {e}")


# Customer.insert_customer(
#     login_id, 
#     cust_name, 
#     identification_id, 
#     phone, 
#     email,
#     membership_id,
#     country
# )

# Booking.insert_booking(
#     book_no, 
#     login_id, 
#     flight_no, 
#     seat_id, 
#     book_time, 
#     boarding_datetime, 
#     departure_airport, 
#     arrival_airport
# )

# %%
