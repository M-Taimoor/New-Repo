import datetime

class Payment:
    def __init__(self, amount, description):
        self.amount = amount
        self.description = description
        self.timestamp = datetime.datetime.now()

class AdHocPayment(Payment):
    def process_payment(self):
        # Logic for processing a one-time ad-hoc payment
        print(f"Processing ad-hoc payment: {self.description} for amount: ${self.amount}")
        # Here you would add integration with a payment gateway

class RecurringPayment(Payment):
    def __init__(self, amount, description, interval):
        super().__init__(amount, description)
        self.interval = interval  # Could be 'monthly', 'weekly', etc.
        self.next_payment_date = self.timestamp + datetime.timedelta(days=self.get_days_until_next_payment())

    def get_days_until_next_payment(self):
        if self.interval == 'monthly':
            return 30  # Simplified monthly interval
        # Add more interval conditions as needed
        return 30

    def process_payment(self):
        # Logic for processing a recurring payment
        print(f"Processing recurring payment: {self.description} for amount: ${self.amount}")
        # Here you would add integration with a payment gateway
        # Update the next payment date
        self.timestamp = datetime.datetime.now()
        self.next_payment_date = self.timestamp + datetime.timedelta(days=self.get_days_until_next_payment())

# Example usage
adhoc_payment = AdHocPayment(100, "Ad-Hoc Service Fee")
adhoc_payment.process_payment()

recurring_payment = RecurringPayment(50, "Monthly Subscription", 'monthly')
recurring_payment.process_payment()