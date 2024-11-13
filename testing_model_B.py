from datetime import datetime, timedelta

class PaymentManager:
    def __init__(self):
        self.adhoc_payments = []
        self.recurring_payments = []
    
    def add_adhoc_payment(self, amount):
        self.adhoc_payments.append({'date': datetime.now(), 'amount': amount})
        print(f"Added adhoc payment of ${amount}.")
    
    def add_recurring_payment(self, amount, interval):
        next_payment_date = datetime.now() + timedelta(days=interval)
        self.recurring_payments.append({'date': next_payment_date, 'amount': amount, 'interval': interval})
        print(f"Added recurring payment of ${amount} every {interval} days.")
    
    def list_payments(self):
        print("Ad-hoc Payments:")
        for payment in self.adhoc_payments:
            print(f"- Amount: ${payment['amount']} on {payment['date']}")
        
        print("\nRecurring Payments:")
        for payment in self.recurring_payments:
            next_payment = payment['date'] + timedelta(days=payment['interval'])
            print(f"- Amount: ${payment['amount']} on {next_payment}")

# Example usage:
payment_system = PaymentManager()
payment_system.add_adhoc_payment(100)
payment_system.add_recurring_payment(50, 30)

payment_system.list_payments()