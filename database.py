#%%
import cx_Oracle

class Database:
    def __init__(self):
        self.user='kenny2'
        self.password='077790'
        self.dsn='XE'
    
    def connect(self):
        try:
            connection= cx_Oracle.connect(user=self.user, password=self.password, dsn=self.dsn)
            print("Connected to Oracle database.")
            return connection
        except cx_Oracle.Error as e:
            print(f"Error connecting to database: {e}")
            return None

# %%
