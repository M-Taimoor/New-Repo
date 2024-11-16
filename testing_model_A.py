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
                interval INTEGER DEFAULT NULL
            )
        ''')
        self.conn.commit()

    # Other methods as defined earlier...

    def list_pending_payments(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM payments WHERE status = 'pending'
        ''')
        pending_payments = cursor.fetchall()
        for payment in pending_payments:
            print(f"ID: {payment[0]}, Amount: {payment[1]}, Date: {payment[2]}, Type: {payment[3]}")
        return pending_payments

    def verify_payment(self, payment_id, expected_amount):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT amount FROM payments WHERE id = ?
        ''', (payment_id,))
        actual_amount = cursor.fetchone()[0]
        return actual_amount == expected_amount

    def generate_report(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT SUM(amount) as total_spent, COUNT(*) as payment_frequency, type FROM payments GROUP BY type
        ''')
        report = cursor.fetchall()
        print("Report:")
        for row in report:
            print(f"Total Spent: {row[0]}, Frequency: {row[1]}, Type: {row[2]}")
        return report

    def export_report_to_csv(self, report, filename='report.csv'):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Total Spent', 'Frequency', 'Type'])
            for row in report:
                writer.writerow(row)

# Example usage:
scheduler = PaymentScheduler()
# Assume other methods and interaction logic have been implemented
report = scheduler.generate_report()
scheduler.export_report_to_csv(report)