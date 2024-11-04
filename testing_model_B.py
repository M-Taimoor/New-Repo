import sqlite3

# Constants
standard_cost_per_hour = 0.5
premium_cost_per_hour = 0.4

# Database setup
conn = sqlite3.connect('streaming_service.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    plan TEXT NOT NULL,
    hours_streamed REAL NOT NULL DEFAULT 0,
    total_cost REAL NOT NULL DEFAULT 0.0
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS plans (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    cost_per_hour REAL NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS billing_history (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    plan_id INTEGER NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    hours_streamed REAL NOT NULL,
    cost_per_hour REAL NOT NULL,
    total_cost REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (plan_id) REFERENCES plans (id)
)
''')

# Insert plans into the database
cursor.execute('INSERT OR IGNORE INTO plans (name, cost_per_hour) VALUES (?, ?)', ('standard', standard_cost_per_hour))
cursor.execute('INSERT OR IGNORE INTO plans (name, cost_per_hour) VALUES (?, ?)', ('premium', premium_cost_per_hour))
conn.commit()

# User Class
class User:
    def __init__(self, username, plan='standard'):
        self.username = username
        self.plan = plan
        self.hours_streamed = 0
        self.total_cost = 0.0
        self.id = self.get_or_create_user()

    def get_or_create_user(self):
        """Get the user id from the database or create a new user."""
        cursor.execute('SELECT id FROM users WHERE username = ?', (self.username,))
        user = cursor.fetchone()
        if user:
            return user[0]
        cursor.execute('INSERT INTO users (username, plan) VALUES (?, ?)', (self.username, self.plan))
        conn.commit()
        return cursor.lastrowid

    def add_usage(self, hours, is_peak_time=False):
        """Track user's streaming hours."""
        self.hours_streamed += hours
        self.save_usage()

    def save_usage(self):
        """Save the user's usage to the billing history."""
        cursor.execute('SELECT cost_per_hour FROM plans WHERE name = ?', (self.plan,))
        cost_per_hour = cursor.fetchone()[0]
        total_cost = self.hours_streamed * cost_per_hour
        if self.plan == 'premium':
            total_cost *= 0.9  # 10% discount for premium users
        cursor.execute('''
        INSERT INTO billing_history (user_id, plan_id, hours_streamed, cost_per_hour, total_cost)
        VALUES (?, (SELECT id FROM plans WHERE name = ?), ?, ?, ?)
        ''', (self.id, self.plan, self.hours_streamed, cost_per_hour, total_cost))
        conn.commit()

    def generate_invoice(self):
        """Generate and display the user’s invoice."""
        cursor.execute('SELECT total_cost FROM billing_history WHERE user_id = ? ORDER BY total_cost DESC LIMIT 5', (self.id,))
        top_five_bills = cursor.fetchall()
        extra_discount = any(total_cost > 100 for total_cost, in top_five_bills)  # 5% extra discount if in top five
        cursor.execute('SELECT name, cost_per_hour FROM plans WHERE name = ?', (self.plan,))
        plan_name, cost_per_hour = cursor.fetchone()

        print(f"Invoice for {self.username}")
        print(f"Plan: {plan_name}")
        print(f"Total Hours Streamed: {self.hours_streamed} hours")
        print(f"Cost per Hour: ${cost_per_hour}")
        print(f"Total Amount Due: ${self.hours_streamed * cost_per_hour}")

        if extra_discount:
            discount_amount = (self.hours_streamed * cost_per_hour) * 0.05
            print(f"Extra 5% Discount: -${discount_amount}")
            print(f"Total Amount After Discount: ${(self.hours_streamed * cost_per_hour) - discount_amount}")
        print(f"Total Amount Due: ${self.hours_streamed * cost_per_hour}\n")

# Example Usage
if __name__ == "__main__":
    # Create a new user and track usage
    user = User("john_doe", plan='premium')
    
    # Simulating usage data
    user.add_usage(5, is_peak_time=True)
    user.add_usage(3)

    # Generate invoice
    user.generate_invoice()

# Close the database connection
conn.close()