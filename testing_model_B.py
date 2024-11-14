import sqlite3
import datetime
import logging
from sqlite3 import Error

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Database setup with error handling
def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        logging.error(e)
    return conn

conn = create_connection('payments.db')
c = conn.cursor()

# Updated database table creation with proper datetime handling
c.execute('''
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor_id INTEGER,
    amount REAL NOT NULL,
    description TEXT NOT NULL,
    payment_type TEXT NOT NULL CHECK(payment_type IN ('ad_hoc', 'recurring')),
    payment_date TEXT NOT NULL
)
''')
conn.commit()

class PaymentError(Exception):
    """Custom exception for payment processing errors"""
    pass

class Payment:
    def __init__(self, vendor_id, amount, description, payment_type):
        self.vendor_id = vendor_id
        self.amount = amount
        self.description = description
        self.payment_type = payment_type
        self.timestamp = datetime.datetime.now().isoformat()

    def process_payment(self):
        # Logic for processing payment
        try:
            print(f"Processing {self.payment_type} payment: {self.description} for amount: ${self.amount}")
            # Here you would add integration with a payment gateway
            # Insert payment record into the database with proper datetime handling
            c.execute('''
            INSERT INTO payments (vendor_id, amount, description, payment_type, payment_date)
            VALUES (?, ?, ?, ?, ?)
            ''', (self.vendor_id, self.amount, self.description, self.payment_type, self.timestamp))
            conn.commit()
        except Error as e:
            logging.error(e)
            raise PaymentError("Failed to process payment transaction.")

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
        # Logic for processing a recurring payment
        try:
            print(f"Processing recurring payment: {self.description} for amount: ${self.amount}")
            # Here you would add integration with a payment gateway
            # Update the next payment date
            self.timestamp = datetime.datetime.now().isoformat()
            self.next_payment_date = self.timestamp + datetime.timedelta(days=self.get_days_until_next_payment())
            # Insert payment record into the database with proper datetime handling
            c.execute('''
            INSERT INTO payments (vendor_id, amount, description, payment_type, payment_date)
            VALUES (?, ?, ?, ?, ?)
            ''', (self.vendor_id, self.amount, self.description, self.payment_type, self.timestamp))
            conn.commit()
        except Error as e:
            logging.error(e)
            raise PaymentError("Failed to process recurring payment transaction.")

# Example usage and functions remain the same as before
# ...

# At the end of the day, show all payments
show_payments()

# Close the database connection
conn.close()