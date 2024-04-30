#%%
from cgitb import text
import email
from multiprocessing import connection
from faker import Faker
import datetime
from matplotlib.pylab import f
import pandas as pd
import numpy as np 
import random
import cx_Oracle
from cust import Customer
from connect import DB
from booking import Booking

fake=Faker()

book_no=[]
login_id=[]
IATA_Code=[] #not done
flight_no=[]
book_time=[]
boarding_date=[]
seat_id=[] 
departure_airport=[] 
arrival_airport=[] 

def rand_time_no_seconds():
    # Generate a random time without seconds
    hour = fake.random_int(min=0, max=23)
    minute = fake.random_int(min=0, max=59)
    return datetime.time(hour=hour, minute=minute)

def rand_datetime_generator(): 
    end_date = datetime.date.today()  # Current date
    start_date = end_date - datetime.timedelta(days=90)  # 90 days ago
    random_date = fake.date_between(start_date=start_date, end_date=end_date)
    random_time = fake.time_object()
    return datetime.datetime.combine(random_date,random_time)

def Airport_MY():
    import random
    international_airports = [
        "John F. Kennedy International Airport (JFK)",
        "Los Angeles International Airport (LAX)",
        "Heathrow Airport (LHR)",
        "Tokyo Haneda Airport (HND)",
        "Beijing Capital International Airport (PEK) ",
        "Dubai International Airport (DXB)",
        # Add more airport names as needed
    ]
    malaysian_airports = [
    "Kuala Lumpur International Airport (KUL)",
    "Penang International Airport (PEN)",
    "Langkawi International Airport (LGK)",
    "Kuching International Airport (KCH)",
    "Kota Kinabalu International Airport (BKI)",
    # Add more Malaysian airports as needed
] 
    depart=random.choice(malaysian_airports)

#randomly choose arrival within local or international
    # remaining_airports= [airport for airport in malaysian_airports if airport != depart]
    arrival_options=international_airports+malaysian_airports
    arrival_options.remove(depart)
    arrival= random.choice(arrival_options)

    return depart , arrival
    
def rand_seat_generator():
    random_letter = random.choice([chr(i) for i in range(65, 91)])
#------------------------------------------------#
# Generate a random numeric part
    numeric_part = fake.numerify(text='##')
#------------------------------------------------#
# Concatenate the random letter and numeric part
    seat = f"{random_letter}{numeric_part}"
    return seat

def Booking_data(book_data):
    book_no=[]
    login_id=[]
    flight_no=[]
    seat_id=[] 
    book_time=[]
    boarding_datetime=[]
    departure_airport=[]
    arrival_airport=[]

    for _ in range(book_data):
        book_no.append(fake.numerify(text='MY######'))
    for _ in range(book_data):
        login_id.append(fake.bothify(text='????###'))
    for _ in range(book_data):
        flight_no.append(fake.random_uppercase_letter() + fake.random_uppercase_letter() + fake.numerify(text='####'))
    for _ in range(book_data):
        random_time = fake.time_object()
        booking_date = rand_datetime_generator()
        book_time.append(datetime.datetime.combine(booking_date, random_time))
    for booking_time in book_time: 
        max_boarding_date = booking_time + datetime.timedelta(days=90)
        boarding_date = fake.date_time_between_dates(booking_time, max_boarding_date)
        boarding_time = rand_time_no_seconds()
        boarding_datetime.append(datetime.datetime.combine(boarding_date, boarding_time))
    for _ in range(book_data):
        departure,arrival = Airport_MY()
        departure_airport.append(departure)
        arrival_airport.append(arrival)
    for _ in range(book_data):
        seat_id.append(rand_seat_generator())


    
    return book_no,login_id,flight_no,book_time,boarding_datetime,departure_airport,arrival_airport,seat_id
book_data=100
book_no,login_id,flight_no,book_time,boarding_datime,departure_airport,arrival_airport,seat_id=Booking_data(book_data)
# # Put the lists into a DataFrame
df = pd.DataFrame({
    'Book_No': book_no,
    'Login_ID': login_id,
    'Flight_No': flight_no,
    'Seat_Id':seat_id,
    'Book_Time': book_time,
    'Boarding_Datetime':boarding_datime,
    'Departure_Airport':departure_airport,
    'Arrival_Airport':arrival_airport

})

df


# connection = cx_Oracle.connect(
#     user="kenny2",
#     password="077790",
#     dsn="XE"
# )

# cursor = connection.cursor()

# # Iterate over the DataFrame rows and insert data into the Oracle table
# for index, row in df.iterrows():
#     cursor.execute("""
#         INSERT INTO Booking (Book_No, Login_ID, Flight_No, Book_Time, Boarding_datetime)
#         VALUES (:1, :2, :3, :4, :5)
#     """, (row['Book_No'], row['Login_ID'], row['Flight_No'], row['Book_Time'], row['Boarding_datetime']))

# # Commit the transaction
# connection.commit()

# # Close the cursor and the connection
# cursor.close()
# connection.close()

# print(len(book_no),len(login_id),len(flight_no),len(book_time),len(boarding_datime))

# %%
