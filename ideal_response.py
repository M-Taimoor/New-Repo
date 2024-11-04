import sqlite3

# Constants
base_cost_per_hour = 0.5  # Default base cost per hour for new plans

# Database setup
conn = sqlite3.connect('streaming_service.db')
cursor = conn.cursor()

# Drop tables if they exist (for development/testing purposes)
cursor.execute('DROP TABLE IF EXISTS users')
cursor.execute('DROP TABLE IF EXISTS plans')
cursor.execute('DROP TABLE IF EXISTS billing_history')

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS plans (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    cost_per_hour REAL NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    plan_id INTEGER,
    hours_streamed REAL NOT NULL DEFAULT 0,
    total_cost REAL NOT NULL DEFAULT 0.0,
    FOREIGN KEY (plan_id) REFERENCES plans (id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS billing_history (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    hours_streamed REAL NOT NULL,
    cost_per_hour REAL NOT NULL,
    total_cost REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

conn.commit()

# User Class
class User:
    def __init__(self, username, plan_name='standard'):
        self.username = username
        self.plan_name = plan_name
        self.hours_streamed = 0
        self.total_cost = 0.0
        self.id = self.get_or_create_user()

    def get_or_create_user(self):
        """Get the user id from the database or create a new user."""
        cursor.execute('SELECT id FROM users WHERE username = ?', (self.username,))
        user = cursor.fetchone()
        if user:
            return user[0]
        
        # Check if the plan exists, if not create it
        cursor.execute('SELECT id FROM plans WHERE name = ?', (self.plan_name,))
        plan = cursor.fetchone()
        if plan:
            plan_id = plan[0]
        else:
            cursor.execute('INSERT INTO plans (name, cost_per_hour) VALUES (?, ?)', (self.plan_name, base_cost_per_hour))
            plan_id = cursor.lastrowid
            conn.commit()
        
        # Insert the new user with the plan_id
        cursor.execute('INSERT INTO users (username, plan_id) VALUES (?, ?)', (self.username, plan_id))
        conn.commit()
        return cursor.lastrowid

    def add_usage(self, hours):
        """Track user's streaming hours."""
        self.hours_streamed += hours
        self.save_usage()

    def calculate_bill(self):
        """Calculate the total cost based on usage."""
        cursor.execute('SELECT cost_per_hour FROM plans WHERE id = ?', (self.get_plan_id(),))
        cost_per_hour = cursor.fetchone()[0]
        self.total_cost = self.hours_streamed * cost_per_hour
        self.check_and_apply_extra_discount()
        return self.total_cost

    def get_plan_id(self):
        """Get the plan id for the user."""
        cursor.execute('SELECT plan_id FROM users WHERE id = ?', (self.id,))
        return cursor.fetchone()[0]

    def save_usage(self):
        """Save the user's usage to the billing history."""
        cost_per_hour = self.calculate_bill() / self.hours_streamed
        cursor.execute('''
        INSERT INTO billing_history (user_id, hours_streamed, cost_per_hour, total_cost)
        VALUES (?, ?, ?, ?)
        ''', (self.id, self.hours_streamed, cost_per_hour, self.total_cost))
        conn.commit()

    def generate_invoice(self):
        """Generate and display the user’s invoice."""
        print(f"Invoice for {self.username}")
        cursor.execute('SELECT name, cost_per_hour FROM plans WHERE id = ?', (self.get_plan_id(),))
        plan_name, cost_per_hour = cursor.fetchone()
        print(f"Plan: {plan_name}")
        print(f"Total Hours Streamed: {self.hours_streamed} hours")
        print(f"Cost per Hour: ${cost_per_hour}")
        print(f"Total Amount Due: ${self.total_cost}\n")

    def check_and_apply_extra_discount(self):
        """Check if the user is among the top 5 highest-billing users and apply extra discount and 1-week free subscription."""
        cursor.execute('''
        SELECT username FROM users ORDER BY total_cost DESC LIMIT 5
        ''')
        top_billing_users = cursor.fetchall()
        if (self.username,) in top_billing_users:
            # Apply extra discount and 1-week free subscription
            print(f"User {self.username} has been awarded an extra discount and 1-week free subscription for being among the top 5 highest-billing users!")

# Example Usage
if __name__ == "__main__":
    # Create a new user and track usage
    user = User("john_doe", plan_name='premium')
    
    # Simulating usage data
    user.add_usage(5)
    user.add_usage(3)

    # Calculate bill and generate invoice
    user.generate_invoice()

# Close the database connection
conn.close()
