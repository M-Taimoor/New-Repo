import sqlite3
import csv
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PaymentScheduler:
    def __init__(self, db_path='payments.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                date DATE NOT NULL,
                type TEXT NOT NULL CHECK (type IN ('recurring', 'adhoc')),
                status TEXT NOT NULL CHECK (status IN ('pending', 'approved', 'processed')),
                vendor TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def schedule_recurring_payment(self, amount, start_date, interval, vendor):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO payments (amount, date, type, status, interval, vendor)
            VALUES (?, ?, 'recurring', 'pending', ?, ?)
        ''', (amount, start_date, interval, vendor))
        self.conn.commit()
        logging.info(f"Recurring payment of {amount} scheduled with vendor {vendor}.")

    def schedule_adhoc_payment(self, amount, date, vendor):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO payments (amount, date, type, status, vendor)
            VALUES (?, ?, 'adhoc', 'pending', ?)
        ''', (amount, date, vendor))
        self.conn.commit()
        logging.info(f"Ad-hoc payment of {amount} scheduled with vendor {vendor}.")

    def initiate_payment(self, payment_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM payments WHERE id = ?', (payment_id,))
        payment = cursor.fetchone()
        if payment:
            logging.info(f"Payment of {payment[1]} initiated, awaiting approval.")
        else:
            logging.error(f"Payment with ID {payment_id} not found.")

    def approve_payment(self, payment_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM payments WHERE id = ?', (payment_id,))
        payment = cursor.fetchone()
        if payment:
            if payment[4] == 'pending':
                cursor.execute('''
                    UPDATE payments SET status = 'approved' WHERE id = ?
                ''', (payment_id,))
                self.conn.commit()
                logging.info(f"Payment of {payment[1]} approved.")
                self.mock_payment_processor(payment[1])
            else:
                logging.error(f"Payment of {payment[1]} is not pending approval.")
        else:
            logging.error(f"Payment with ID {payment_id} not found.")

    def process_payments(self):
        cursor = self.conn.cursor()
        today = datetime.now().date()
        # Process recurring payments
        cursor.execute('''
            SELECT * FROM payments WHERE date <= ? AND type = 'recurring' AND status = 'approved'
        ''', (today,))
        for payment in cursor.fetchall():
            self.initiate_payment(payment[0])
            next_date = datetime.strptime(payment[2], '%Y-%m-%d').date() + timedelta(days=payment[5])
            cursor.execute('''
                UPDATE payments SET date = ? WHERE id = ?
            ''', (next_date, payment[0]))
            self.conn.commit()

        # Process ad-hoc payments
        cursor.execute('''
            SELECT * FROM payments WHERE date <= ? AND type = 'adhoc' AND status = 'approved'
        ''', (today,))
        for payment in cursor.fetchall():
            self.initiate_payment(payment[0])

    def list_pending_payments(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM payments WHERE status = 'pending'
        ''')
        pending_payments = cursor.fetchall()
        for payment in pending_payments:
            print(f"ID: {payment[0]}, Amount: {payment[1]}, Date: {payment[2]}, Vendor: {payment[5]}")
        return pending_payments

    def mock_payment_processor(self, amount):
        print(f"Payment of {amount} processed.")

    def __del__(self):
        self.conn.close()

# Example usage
scheduler = PaymentScheduler()
scheduler.schedule_recurring_payment(amount=1000, start_date='2023-04-01', interval=30, vendor='Vendor A') # Monthly
scheduler.schedule_adhoc_payment(amount=500, date='2023-04-06', vendor='Vendor B') # 5 days from now
scheduler.process_payments()
scheduler.approve_payment(1) # Approve the first payment

# Command-line interface
while True:
    print("\nCommands: add, view, approve, process, report, export, quit")
    command = input("Enter command: ").lower()
    if command == 'add':
        amount = float(input("Enter amount: "))
        date = input("Enter date (YYYY-MM-DD): ")
        type = input("Enter type (recurring/adhoc): ")
        vendor = input("Enter vendor name: ")
        if type == 'recurring':
            interval = int(input("Enter interval in days: "))
            scheduler.schedule_recurring_payment(amount, date, interval, vendor)
        else:
            scheduler.schedule_adhoc_payment(amount, date, vendor)
    elif command == 'view':
        scheduler.list_pending_payments()
    elif command == 'approve':
        payment_id = int(input("Enter payment ID to approve: "))
        scheduler.approve_payment(payment_id)
    elif command == 'process':
        scheduler.process_payments()
    elif command == 'report':
        # Generate summary report
        cursor = scheduler.conn.cursor()
        cursor.execute('SELECT vendor, SUM(amount) as total_spent, COUNT(*) as payment_count FROM payments WHERE status = 'processed' GROUP BY vendor')
        for row in cursor.fetchall():
            print(f"Vendor: {row[0]}, Total Spent: {row[1]}, Payment Count: {row[2]}")
    elif command == 'export':
        filename = input("Enter filename for CSV export: ")
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Amount', 'Date', 'Vendor'])
            cursor = scheduler.conn.cursor()
            cursor.execute('SELECT * FROM payments WHERE status = 'processed'')
            for payment in cursor.fetchall():
                writer.writerow(payment)
        print(f"Report exported to {filename}.")
    elif command == 'quit':
        break
    else:
        print("Invalid command.")