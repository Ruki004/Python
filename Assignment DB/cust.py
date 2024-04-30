#%%
from tkinter.ttk import Separator
from faker import Faker

fake=Faker()

class Customer:
    def __init__(self,connection):
        self.connection = connection
        
        pass
    @staticmethod
    def generate_login_id():
        return fake.bothify(text='????###')
    
    @staticmethod
    def generate_name():
        random_name = fake.name()
        return random_name
    
    @staticmethod
    def generate_gender():
        import secrets
        gender_options = ["F", "M"]
        random_gender = secrets.choice(gender_options)
        return random_gender
    
    @staticmethod
    def generate_identification_id():
        import random
        # Generate a random string of 10 digits
        digits = ''.join(random.choices('0123456789', k=10))
        # Insert a hyphen at a random position
        position = random.randint(1, 9)  # Position must be between 1 and 9 to leave room for the hyphen
        identification_id = digits[:position] + '-' + digits[position:]
        return identification_id
    
    @staticmethod
    def generate_email():
        domain = fake.random_element(elements=('gmail.com', 'yahoo.com', 'outlook.com'))
        max_username_length = 25 - len(domain) - 1  # Account for "@" symbol
        username = fake.user_name()[:max_username_length]
        return f"{username}@{domain}"
        
    @staticmethod
    def generate_membership_id():
        import random
            # Generate a random membership ID with "AAS" followed by 5 random numbers
        membership_id = f"AAS{random.randint(10000, 99999)}"
        return membership_id
    
    @staticmethod
    def generate_country():
        country = fake.country()
        return country
    
    @staticmethod
    def generate_phone():
        import random
        # Generate the remaining 9 digits
        remaining_digits = ''.join(random.choices('0123456789', k=9))
        # Concatenate with the country code "+60"
        phone_number = "+60" + remaining_digits
        return phone_number

    def insert_customer(self,login_id, password, cust_name,identification_id, phone, email,membership_id,country):
        cursor = self.connection.cursor()
        try:  
            for i in range(len(login_id)):
                cursor.execute("""
                    INSERT INTO Customer (Login_ID, Password, Cust_Name,Identification_id,Phone, Email, Membership_Id, Country)
                    VALUES (:1,:2,:3,:4,:5,:6,:7,:8)
                """, (login_id[i], password[i], cust_name[i],identification_id[i],phone[i],email[i],membership_id[i],country[i]))
            self.connection.commit()
            print("Customer inserted successfully.")
        except Exception as e:
            print(f"Error inserting bookings: {e}")
        finally:
            cursor.close()

    
    

    
    
# %%
