import sqlite3
import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Database setup with error handling
try:
    conn = sqlite3.connect('payments.db')
    c = conn.cursor()
    
    # Create tables for vendors and payments with error handling
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
        payment_date TEXT NOT NULL,
        FOREIGN KEY (vendor_id) REFERENCES vendors (id)
    )
    ''')
    conn.commit()
except sqlite3.Error as e:
    logging.error(f"Error setting up database: {e}")
    conn.close()
    raise SystemExit

class Payment:
    def __init__(self, vendor_id, amount, description, payment_type):
        self.vendor_id = vendor_id
        self.amount = amount
        self.description = description
        self.payment_type = payment_type
        self.timestamp = datetime.datetime.now()  # Store as a datetime object for easy manipulation

    def process_payment(self):
        try:
            # Logic for processing payment
            logging.info(f"Processing {self.payment_type} payment: {self.description} for amount: ${self.amount}")
            # Insert payment record into the database
            c.execute('''
            INSERT INTO payments (vendor_id, amount, description, payment_type, payment_date)
            VALUES (?, ?, ?, ?, ?)
            ''', (self.vendor_id, self.amount, self.description, self.payment_type, self.timestamp.isoformat()))
            conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Failed to process payment: {e}")
            conn.rollback()

class AdHocPayment(Payment):
    pass  # No additional attributes for ad-hoc payments

class RecurringPayment(Payment):
    def __init__(self, vendor_id, amount, description, payment_type, interval):
        super().__init__(vendor_id, amount, description, payment_type)
        self.interval = interval  # Could be 'monthly', 'weekly', etc.
        self.next_payment_date = self.calculate_next_payment_date()

    def get_days_until_next_payment(self):
        if self.interval == 'monthly':
            return 30  # Simplified monthly interval
        elif self.interval == 'weekly':
            return 7  # Example interval
        else:
            logging.warning(f"Unsupported interval '{self.interval}' specified, defaulting to monthly.")
            return 30  # Default to 30 days if unsupported interval

    def calculate_next_payment_date(self):
        # Calculate the next payment date based on the interval
        return self.timestamp + datetime.timedelta(days=self.get_days_until_next_payment())

    def process_payment(self):
        try:
            # Logic for processing a recurring payment
            logging.info(f"Processing recurring payment: {self.description} for amount: ${self.amount}")
            # Update the next payment date
            self.timestamp = datetime.datetime.now()
            self.next_payment_date = self.calculate_next_payment_date()
            # Insert payment record into the database
            c.execute('''
            INSERT INTO payments (vendor_id, amount, description, payment_type, payment_date)
            VALUES (?, ?, ?, ?, ?)
            ''', (self.vendor_id, self.amount, self.description, self.payment_type, self.timestamp.isoformat()))
            conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Failed to process recurring payment: {e}")
            conn.rollback()

# Example usage with error handling
try:
    # Assume vendor with id 1 already exists in the database
    vendor_id = 1
    adhoc_payment = AdHocPayment(vendor_id, 100, "Ad-Hoc Service Fee", 'ad_hoc')
    adhoc_payment.process_payment()

    recurring_payment = RecurringPayment(vendor_id, 50, "Monthly Subscription", 'recurring', 'monthly')
    recurring_payment.process_payment()

    # Function to show all ad-hoc and recurring payments at the end of the day
    def show_payments():
        try:
            c.execute('SELECT * FROM payments WHERE payment_type = "ad_hoc" OR payment_type = "recurring"')
            payments = c.fetchall()
            for payment in payments:
                print(payment)
        except sqlite3.Error as e:
            logging.error(f"Error fetching payments: {e}")

    # At the end of the day, show all payments
    show_payments()

except Exception as e:
    logging.error(f"An error occurred during payment processing: {e}")

finally:
    # Close the database connection
    conn.close()
    logging.info("Database connection closed.")
