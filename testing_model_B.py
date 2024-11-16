import sqlite3
import logging
import csv
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
                interval INTEGER DEFAULT NULL,
                vendor TEXT DEFAULT NULL
            )
        ''')
        self.conn.commit()

    # Existing methods ...

    def list_pending_payments(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM payments WHERE status = 'pending'
        ''')
        pending_payments = cursor.fetchall()
        print("Pending Payments:")
        for payment in pending_payments:
            print(payment)

    def verify_payment(self, payment_id, expected_amount):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM payments WHERE id = ?', (payment_id,))
        payment = cursor.fetchone()
        if payment and payment[1] == expected_amount:
            print("Payment verified successfully.")
            return True
        else:
            print("Payment verification failed.")
            return False

    def generate_report(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT vendor, COUNT(*) as frequency, SUM(amount) as total_spent
            FROM payments
            WHERE status = 'processed'
            GROUP BY vendor
            ORDER BY total_spent DESC
        ''')
        return cursor.fetchall()

    def export_report_to_csv(self, report_data, filename='report.csv'):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Vendor', 'Frequency', 'Total Spent'])
            for data in report_data:
                writer.writerow(data)
        print(f"Report exported to {filename}.")

    def command_line_interface(self):
        while True:
            print("\nPayment Scheduler CLI")
            print("1. Schedule Recurring Payment")
            print("2. Schedule Ad-hoc Payment")
            print("3. List Pending Payments")
            print("4. Approve Payment")
            print("5. Process Payments")
            print("6. Generate Report")
            print("7. Export Report to CSV")
            print("8. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                amount = float(input("Enter amount: "))
                start_date = input("Enter start date (YYYY-MM-DD): ")
                interval = int(input("Enter interval in days: "))
                self.schedule_recurring_payment(amount, start_date, interval)
            elif choice == '2':
                amount = float(input("Enter amount: "))
                date = input("Enter date (YYYY-MM-DD): ")
                self.schedule_adhoc_payment(amount, date)
            elif choice == '3':
                self.list_pending_payments()
            elif choice == '4':
                payment_id = int(input("Enter payment ID to approve: "))
                self.approve_payment(payment_id)
            elif choice == '5':
                self.process_payments()
            elif choice == '6':
                report = self.generate_report()
                for row in report:
                    print(row)
            elif choice == '7':
                report = self.generate_report()
                self.export_report_to_csv(report)
            elif choice == '8':
                print("Exiting CLI.")
                break
            else:
                print("Invalid choice. Please try again.")

# Example usage:
scheduler = PaymentScheduler()
scheduler.command_line_interface()