import sqlite3
from contextlib import closing

# Path to the SQLite database file
DATABASE_PATH = 'bank.db'

# Function to initialize the database and create the 'accounts' table if it doesn't exist
def initialize_database():
    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    balance REAL NOT NULL
                )
            ''')
            connection.commit()

# Function to create a new account securely
def create_account(name, initial_balance):
    try:
        with closing(sqlite3.connect(DATABASE_PATH)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute('INSERT INTO accounts (name, balance) VALUES (?, ?)', (name, initial_balance))
                connection.commit()
        return f"Account '{name}' created successfully with balance {initial_balance}"
    except sqlite3.DatabaseError as e:
        return f"Error creating account: {e}"

# Function to retrieve the balance of an account securely
def get_account_balance(account_name):
    try:
        with closing(sqlite3.connect(DATABASE_PATH)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute('SELECT name, balance FROM accounts WHERE name = ?', (account_name,))
                account = cursor.fetchone()
                if account:
                    return f"Account: {account[0]}, Balance: {account[1]}"
                else:
                    return "Account not found"
    except sqlite3.DatabaseError as e:
        return f"Error retrieving account balance: {e}"

# Example usage
if __name__ == "__main__":
    # Initialize the database (create the 'accounts' table if not exists)
    initialize_database()

    # Create a new account
    print(create_account('John Doe', 1000.0))
    
    # Retrieve the balance for 'John Doe'
    print(get_account_balance('John Doe'))
