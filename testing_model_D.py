import sqlite3

# Database setup
conn = sqlite3.connect('streaming_service.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    user_type TEXT NOT NULL,
    plan_id INTEGER NOT NULL,
    FOREIGN KEY (plan_id) REFERENCES plans (id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS plans (
    id INTEGER PRIMARY KEY,
    plan_name TEXT NOT NULL,
    cost_per_hour REAL NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS billing_history (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    hours_streamed REAL NOT NULL,
    total_cost REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS discounts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    discount_amount REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

conn.commit()

# Insert plans into the plans table
plans = [
    (1, 'standard', 0.5),
    (2, 'premium', 0.4)  # Premium users have a lower cost per hour
]
cursor.executemany('INSERT OR IGNORE INTO plans (id, plan_name, cost_per_hour) VALUES (?, ?, ?)', plans)
conn.commit()

# User Class
class User:
    def __init__(self, username, user_type='regular', plan_id=1):
        self.username = username
        self.user_type = user_type
        self.plan_id = plan_id
        self.hours_streamed = 0
        self.total_cost = 0.0
        self.id = self.get_or_create_user()

    def get_or_create_user(self):
        """Get the user id from the database or create a new user."""
        cursor.execute('SELECT id FROM users WHERE username = ?', (self.username,))
        user = cursor.fetchone()
        if user:
            return user[0]
        cursor.execute('INSERT INTO users (username, user_type, plan_id) VALUES (?, ?, ?)', (self.username, self.user_type, self.plan_id))
        conn.commit()
        return cursor.lastrowid

    def add_usage(self, hours, is_peak_time=False):
        """Track user's streaming hours."""
        self.hours_streamed += hours
        self.calculate_bill(is_peak_time)

    def calculate_bill(self, is_peak_time):
        """Calculate the total cost based on usage."""
        plan_cost = self.get_plan_cost()
        self.total_cost = self.hours_streamed * plan_cost
        if is_peak_time:
            self.total_cost *= 1.2  # 20% increase during peak times
        if self.user_type == 'premium':
            self.apply_discount()

    def get_plan_cost(self):
        """Get the cost per hour for the user's plan."""
        cursor.execute('SELECT cost_per_hour FROM plans WHERE id = ?', (self.plan_id,))
        plan = cursor.fetchone()
        return plan[0] if plan else base_cost_per_hour

    def apply_discount(self):
        """Apply a promotional discount to the user."""
        cursor.execute('SELECT cost_per_hour FROM plans WHERE id = ?', (self.plan_id,))
        plan = cursor.fetchone()
        if plan:
            self.total_cost *= 0.9  # 10% discount for premium users

    def save_usage(self):
        """Save the user's usage to the billing history."""
        cursor.execute('''
        INSERT INTO billing_history (user_id, hours_streamed, total_cost)
        VALUES (?, ?, ?)
        ''', (self.id, self.hours_streamed, self.total_cost))
        conn.commit()

    def generate_invoice(self):
        """Generate and display the user’s invoice."""
        print(f"Invoice for {self.username}")
        print(f"User Type: {self.user_type}")
        print(f"Plan: {self.get_plan_name()}")
        print(f"Total Hours Streamed: {self.hours_streamed} hours")
        print(f"Total Amount Due: ${self.total_cost}\n")

    def get_plan_name(self):
        """Get the name of the user's plan."""
        cursor.execute('SELECT plan_name FROM plans WHERE id = ?', (self.plan_id,))
        plan = cursor.fetchone()
        return plan[0] if plan else 'Unknown'

# Example Usage
if __name__ == "__main__":
    # Create a new user and track usage
    user = User("john_doe", user_type='premium')
    
    # Simulating usage data
    user.add_usage(5, is_peak_time=True)
    user.add_usage(3)

    # Calculate bill and generate invoice
    user.generate_invoice()

    # Close the database connection
    conn.close()