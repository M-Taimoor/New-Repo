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
                vendor TEXT NOT NULL,
                interval INTEGER DEFAULT NULL
            )
        ''')
        self.conn.commit()

    def schedule_recurring_payment(self, amount, start_date, interval, vendor):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO payments (amount, date, type, status, vendor, interval)
            VALUES (?, ?, 'recurring', 'pending', ?, ?)
        ''', (amount, start_date, vendor, interval))
        self.conn.commit()
        logging.info(f"Recurring payment of {amount} scheduled.")

    def schedule_adhoc_payment(self, amount, date, vendor):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO payments (amount, date, type, status, vendor)
            VALUES (?, ?, 'adhoc', 'pending', ?)
        ''', (amount, date, vendor))
        self.conn.commit()
        logging.info(f"Ad-hoc payment of {amount} scheduled.")

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
        cursor.execute('SELECT * FROM payments WHERE status = "pending"')
        pending_payments = cursor.fetchall()
        print("Pending Payments:")
        for payment in pending_payments:
            print(f"ID: {payment[0]}, Amount: {payment[1]}, Date: {payment[2]}, Vendor: {payment[5]}")

    def verify_payment(self, payment_id, expected_amount):
        cursor = self.conn.cursor()
        cursor.execute('SELECT amount FROM payments WHERE id = ?', (payment_id,))
        actual_amount = cursor.fetchone()[0]
        return actual_amount == expected_amount

    def generate_report(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT vendor, COUNT(*) AS frequency, SUM(amount) AS total_spent
            FROM payments
            GROUP BY vendor
            ORDER BY total_spent DESC
        ''')
        report = cursor.fetchall()
        print("Spending Report:")
        for vendor, frequency, total_spent in report:
            print(f"Vendor: {vendor}, Frequency: {frequency}, Total Spent: {total_spent}")
        return report

    def export_report_to_csv(self, report, filename='report.csv'):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Vendor', 'Frequency', 'Total Spent'])
            for row in report:
                writer.writerow(row)

    def mock_payment_processor(self, amount):
        print(f"Payment of {amount} processed.")

    def __del__(self):
        self.conn.close()

    def run_cli(self):
        while True:
            print("\nCommands:")
            print("1. Add recurring payment")
            print("2. Add ad-hoc payment")
            print("3. List pending payments")
            print("4. Approve payment")
            print("5. Process payments")
            print("6. Generate report")
            print("7. Export report to CSV")
            print("8. Exit")
            command = input("Enter command number: ")
            if command == '1':
                amount = float(input("Enter amount: "))
                start_date = input("Enter start date (YYYY-MM-DD): ")
                interval = int(input("Enter interval (days): "))
                vendor = input("Enter vendor: ")
                self.schedule_recurring_payment(amount, start_date, interval, vendor)
            elif command == '2':
                amount = float(input("Enter amount: "))
                date = input("Enter date (YYYY-MM-DD): ")
                vendor = input("Enter vendor: ")
                self.schedule_adhoc_payment(amount, date, vendor)
            elif command == '3':
                self.list_pending_payments()
            elif command == '4':
                payment_id = int(input("Enter payment ID to approve: "))
                self.approve_payment(payment_id)
            elif command == '5':
                self.process_payments()
            elif command == '6':
                report = self.generate_report()
                print(report)
            elif command == '7':
                if 'report' not in locals():
                    print("No report generated. Generate a report first.")
                else:
                    filename = input("Enter filename for the CSV export: ")
                    self.export_report_to_csv(report, filename)
                    print(f"Report exported to {filename}")
            elif command == '8':
                break
            else:
                print("Invalid command.")

# Example usage:
scheduler = PaymentScheduler()
scheduler.run_cli()