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
    hours_streamed REAL NOT NULL DEFAULT 0,
    total_cost REAL NOT NULL DEFAULT 0.0
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
    plan_id INTEGER NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    hours_streamed REAL NOT NULL,
    cost_per_hour REAL NOT NULL,
    total_cost REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (plan_id) REFERENCES plans (id)
)
''')

# Insert default plans
plans = [
    ('standard', 0.5),
    ('premium', 0.4)  # Premium users get a lower rate per hour
]
cursor.executemany('INSERT OR IGNORE INTO plans (plan_name, cost_per_hour) VALUES (?, ?)', plans)

conn.commit()

# User Class
class User:
    def __init__(self, username, user_type='regular'):
        self.username = username
        self.user_type = user_type
        self.hours_streamed = 0
        self.total_cost = 0.0
        self.plan_id = 2 if user_type == 'premium' else 1  # Assuming premium is ID 2 and standard is ID 1
        self.id = self.get_or_create_user()

    def get_or_create_user(self):
        """Get the user id from the database or create a new user."""
        cursor.execute('SELECT id FROM users WHERE username = ?', (self.username,))
        user = cursor.fetchone()
        if user:
            return user[0]
        cursor.execute('INSERT INTO users (username, user_type) VALUES (?, ?)', (self.username, self.user_type))
        conn.commit()
        return cursor.lastrowid

    def add_usage(self, hours, is_peak_time=False):
        """Track user's streaming hours."""
        self.hours_streamed += hours
        self.save_usage()

    def calculate_bill(self):
        """Calculate the total cost based on usage."""
        cursor.execute('SELECT cost_per_hour FROM plans WHERE id = ?', (self.plan_id,))
        cost_per_hour = cursor.fetchone()[0]
        self.total_cost = self.hours_streamed * cost_per_hour
        return self.total_cost

    def save_usage(self):
        """Save the user's usage to the billing history."""
        cursor.execute('SELECT cost_per_hour FROM plans WHERE id = ?', (self.plan_id,))
        cost_per_hour = cursor.fetchone()[0]
        cursor.execute('''
        INSERT INTO billing_history (user_id, plan_id, hours_streamed, cost_per_hour, total_cost)
        VALUES (?, ?, ?, ?, ?)
        ''', (self.id, self.plan_id, self.hours_streamed, cost_per_hour, self.total_cost))
        conn.commit()

    def generate_invoice(self):
        """Generate and display the user’s invoice."""
        print(f"Invoice for {self.username}")
        print(f"User Type: {self.user_type}")
        print(f"Total Hours Streamed: {self.hours_streamed} hours")
        print(f"Total Amount Due: ${self.calculate_bill()}\n")

    def apply_discount(self):
        """Apply a promotional discount to the user."""
        # Apply extra discount for top 5 users with the highest billing
        cursor.execute('''
        SELECT user_id FROM billing_history
        GROUP BY user_id
        ORDER BY SUM(total_cost) DESC
        LIMIT 5
        ''')
        top_users = [user[0] for user in cursor.fetchall()]
        if self.id in top_users:
            self.total_cost *= 0.9  # 10% extra discount
            print(f"User {self.username} has received an extra 10% discount and 1 week of free subscription!")

# Example Usage
if __name__ == "__main__":
    # Create a new user and track usage
    user = User("john_doe", user_type='premium')
    
    # Simulating usage data
    user.add_usage(5, is_peak_time=True)
    user.add_usage(3)

    # Calculate bill and generate invoice
    user.generate_invoice()

    # Apply discounts for top 5 users
    user.apply_discount()

    # Close the database connection
    conn.close()