import sqlite3
import datetime

# Database setup
conn = sqlite3.connect('payments.db')
c = conn.cursor()

# Create tables for vendors and payments
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

class PaymentProcessingError(Exception):
    pass

class Payment:
    def __init__(self, vendor_id, amount, description, payment_type):
        self.vendor_id = vendor_id
        self.amount = amount
        self.description = description
        self.payment_type = payment_type
        self.timestamp = datetime.datetime.now()

    def process_payment(self):
        try:
            # Logic for processing payment
            print(f"Processing {self.payment_type} payment: {self.description} for amount: ${self.amount}")
            # Simulated payment processing
            if self.amount <= 0:
                raise ValueError("Payment amount must be greater than 0.")
            # Here you would add integration with a payment gateway
            # Insert payment record into the database
            c.execute('''
            INSERT INTO payments (vendor_id, amount, description, payment_type, payment_date)
            VALUES (?, ?, ?, ?, ?)
            ''', (self.vendor_id, self.amount, self.description, self.payment_type, self.timestamp))
            conn.commit()
        except (sqlite3.DatabaseError, ValueError) as e:
            # Log payment processing error
            print(f"Payment processing failed: {e}")
            raise PaymentProcessingError(e)

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
            self.timestamp = datetime.datetime.now()
            self.next_payment_date = self.timestamp + datetime.timedelta(days=self.get_days_until_next_payment())
            # Insert payment record into the database
            c.execute('''
            INSERT INTO payments (vendor_id, amount, description, payment_type, payment_date)
            VALUES (?, ?, ?, ?, ?)
            ''', (self.vendor_id, self.amount, self.description, self.payment_type, self.timestamp))
            conn.commit()
        except (sqlite3.DatabaseError, ValueError) as e:
            # Log payment processing error
            print(f"Recurring payment processing failed: {e}")
            raise PaymentProcessingError(e)

# Example usage
# Assume vendor with id 1 already exists in the database
vendor_id = 1
adhoc_payment = AdHocPayment(vendor_id, 100, "Ad-Hoc Service Fee", 'ad_hoc')
try:
    adhoc_payment.process_payment()
except PaymentProcessingError:
    print("Ad-hoc payment failed to process.")

recurring_payment = RecurringPayment(vendor_id, 50, "Monthly Subscription", 'recurring', 'monthly')
try:
    recurring_payment.process_payment()
except PaymentProcessingError:
    print("Recurring payment failed to process.")

# Function to show all ad-hoc and recurring payments at the end of the day
def show_payments():
    c.execute('SELECT * FROM payments WHERE payment_type = "ad_hoc" OR payment_type = "recurring"')
    payments = c.fetchall()
    for payment in payments:
        print(payment)

# At the end of the day, show all payments
show_payments()

# Close the database connection
conn.close()