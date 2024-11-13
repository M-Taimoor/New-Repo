from datetime import datetime, timedelta
import uuid

# Define a simple Payment class to store payment details
class Payment:
    def __init__(self, amount, recipient, payment_type="adhoc", frequency=None):
        self.id = uuid.uuid4()
        self.amount = amount
        self.recipient = recipient
        self.payment_type = payment_type  # 'adhoc' or 'recurring'
        self.frequency = frequency  # e.g., 'monthly' for recurring payments
        self.created_at = datetime.now()
        self.next_payment_date = self.schedule_next_payment()

    def schedule_next_payment(self):
        if self.payment_type == "recurring" and self.frequency:
            if self.frequency == "monthly":
                return self.created_at + timedelta(days=30)
        return self.created_at  # For ad-hoc, next payment is the creation time

    def authorize_payment(self):
        print(f"Authorizing payment ID {self.id} of amount ${self.amount} to {self.recipient}.")

    def process_payment(self):
        print(f"Processing payment ID {self.id} of amount ${self.amount} to {self.recipient} on {datetime.now()}.")

# Define a PaymentSystem class to manage multiple payments
class PaymentSystem:
    def __init__(self):
        self.payments = []

    def add_payment(self, payment):
        self.payments.append(payment)
        print(f"Payment to {payment.recipient} added.")

    def schedule_payments(self):
        for payment in self.payments:
            if payment.payment_type == "recurring" and payment.next_payment_date <= datetime.now():
                payment.authorize_payment()
                payment.process_payment()
                payment.next_payment_date = payment.schedule_next_payment()  # Update for next cycle

    def report_spending(self):
        print("\nSpending Report:")
        spending_summary = {}
        for payment in self.payments:
            spending_summary[payment.recipient] = spending_summary.get(payment.recipient, 0) + payment.amount
        for recipient, total in spending_summary.items():
            print(f"Total paid to {recipient}: ${total}")

# Sample Usage
if __name__ == "__main__":
    payment_system = PaymentSystem()

    # Add an ad-hoc payment
    adhoc_payment = Payment(amount=500, recipient="Service Provider A", payment_type="adhoc")
    payment_system.add_payment(adhoc_payment)

    # Add a recurring monthly payment
    recurring_payment = Payment(amount=2000, recipient="Supplier B", payment_type="recurring", frequency="monthly")
    payment_system.add_payment(recurring_payment)

    # Simulate scheduling and processing payments
    print("\nScheduling payments:")
    payment_system.schedule_payments()

    # Generate spending report
    payment_system.report_spending()
