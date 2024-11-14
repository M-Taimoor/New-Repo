import sqlite3
import datetime
import logging
from sqlite3 import Error

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Database setup with error handling
def create_connection(db_file):
    """ create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        logging.error(e)
    return conn

conn = create_connection('payments.db')

# Create tables for vendors and payments with error handling
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        logging.error(e)

sql_create_vendors_table = '''
CREATE TABLE IF NOT EXISTS vendors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    address TEXT NOT NULL
)
'''

sql_create_payments_table = '''
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor_id INTEGER,
    amount REAL NOT NULL,
    description TEXT NOT NULL,
    payment_type TEXT NOT NULL CHECK(payment_type IN ('ad_hoc', 'recurring')),
    payment_date TIMESTAMP NOT NULL,
    FOREIGN KEY (vendor_id) REFERENCES vendors (id)
)
'''

if conn is not None:
    create_table(conn, sql_create_vendors_table)
    create_table(conn, sql_create_payments_table)
else:
    logging.error("Error! cannot create the database connection.")

# Payment processing classes with error handling
class Payment:
    def __init__(self, vendor_id, amount, description, payment_type):
        self.vendor_id = vendor_id
        self.amount = amount
        self.description = description
        self.payment_type = payment_type
        self.timestamp = datetime.datetime.now().isoformat()

    def process_payment(self):
        try:
            # Logic for processing payment
            print(f"Processing {self.payment_type} payment: {self.description} for amount: ${self.amount}")
            # Here you would add integration with a payment gateway
            # Insert payment record into the database
            with conn:
                conn.execute('''
                INSERT INTO payments (vendor_id, amount, description, payment_type, payment_date)
                VALUES (?, ?, ?, ?, ?)
                ''', (self.vendor_id, self.amount, self.description, self.payment_type, self.timestamp))
        except Error as e:
            logging.error(e)
        except Exception as e:
            logging.error(f"An error occurred while processing the payment: {e}")

class AdHocPayment(Payment):
    pass  # No additional attributes for ad-hoc payments

class RecurringPayment(Payment):
    def __init__(self, vendor_id, amount, description, payment_type, interval):
        super().__init__(vendor_id, amount, description, payment_type)
        self.interval = interval  # Could be 'monthly', 'weekly', etc.
        self.next_payment_date = self.timestamp + datetime.timedelta(days=self.get_days_until_next_payment())

    def get_days_until_next_payment(self):
        if self.interval == 'monthly':
            return 30  # Simplified monthly interval
        # Add more interval conditions as needed
        return 30

    def process_payment(self):
        try:
            # Logic for processing a recurring payment
            print(f"Processing recurring payment: {self.description} for amount: ${self.amount}")
            # Here you would add integration with a payment gateway
            # Update the next payment date
            self.timestamp = datetime.datetime.now().isoformat()
            self.next_payment_date = self.timestamp + datetime.timedelta(days=self.get_days_until_next_payment())
            # Insert payment record into the database
            with conn:
                conn.execute('''
                INSERT INTO payments (vendor_id, amount, description, payment_type, payment_date)
                VALUES (?, ?, ?, ?, ?)
                ''', (self.vendor_id, self.amount, self.description, self.payment_type, self.timestamp))
        except Error as e:
            logging.error(e)
        except Exception as e:
            logging.error(f"An error occurred while processing the recurring payment: {e}")

# Example usage
# Assume vendor with id 1 already exists in the database
vendor_id = 1
try:
    adhoc_payment = AdHocPayment(vendor_id, 100, "Ad-Hoc Service Fee", 'ad_hoc')
    adhoc_payment.process_payment()

    recurring_payment = RecurringPayment(vendor_id, 50, "Monthly Subscription", 'recurring', 'monthly')
    recurring_payment.process_payment()

    # Function to show all ad-hoc and recurring payments at the end of the day
    def show_payments():
        try:
            with conn:
                conn.execute('SELECT * FROM payments WHERE payment_type = "ad_hoc" OR payment_type = "recurring"')
                payments = conn.fetchall()
                for payment in payments:
                    print(payment)
        except Error as e:
            logging.error(e)

    # At the end of the day, show all payments
    show_payments()
finally:
    # Close the database connection
    if conn:
        conn.close()