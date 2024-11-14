import sqlite3
import datetime
import pytz
from sqlite3 import Error

# Function to create a database connection
def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file"""
    conn = None
    try:
        conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        return conn
    except Error as e:
        print(e)
    return conn

# Function to create tables for vendors and payments
def create_tables(conn):
    """Create vendors and payments tables"""
    try:
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS vendors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL
        )
        ''')
        c.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor_id INTEGER,
            amount REAL NOT NULL,
            description TEXT NOT NULL,
            payment_type TEXT NOT NULL CHECK(payment_type IN ('ad_hoc', 'recurring')),
            payment_date TIMESTAMP NOT NULL,
            FOREIGN KEY (vendor_id) REFERENCES vendors (id)
        )
        ''')
        conn.commit()
    except Error as e:
        print(e)

# Database setup
conn = create_connection('payments.db')
create_tables(conn)

class Payment:
    def __init__(self, vendor_id, amount, description, payment_type):
        self.vendor_id = vendor_id
        self.amount = amount
        self.description = description
        self.payment_type = payment_type
        self.timestamp = datetime.datetime.now(pytz.utc)

    def process_payment(self):
        try:
            # Logic for processing payment
            print(f"Processing {self.payment_type} payment: {self.description} for amount: ${self.amount}")
            # Here you would add integration with a payment gateway
            # Insert payment record into the database
            c.execute('''
            INSERT INTO payments (vendor_id, amount, description, payment_type, payment_date)
            VALUES (?, ?, ?, ?, ?)
            ''', (self.vendor_id, self.amount, self.description, self.payment_type, self.timestamp))
            conn.commit()
        except Error as e:
            print(f"An error occurred while processing the payment: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Additional classes and functions as in previous example...

# At the end of the day, show all payments
def show_payments(conn):
    try:
        c = conn.cursor()
        c.execute('SELECT * FROM payments WHERE payment_type = "ad_hoc" OR payment_type = "recurring"')
        payments = c.fetchall()
        for payment in payments:
            print(payment)
    except Error as e:
        print(f"An error occurred while fetching payments: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Use the show_payments function
show_payments(conn)

# Close the database connection
conn.close()