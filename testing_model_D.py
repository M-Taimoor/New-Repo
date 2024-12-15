import random
import string
import time
from datetime import datetime, timedelta
import sqlite3

# Constants
OTP_LENGTH_RANGE = (4, 8)
MAX_FAILED_LOGIN_ATTEMPTS = 3
OTP_EXPIRY_TIME = 5  # minutes
SECURITY_QUESTIONS = {
    "What is your mother's maiden name?": "Smith",
    "What was the name of your first pet?": "Fluffy",
    "What is your favorite color?": "Blue",
}

class User:
    def __init__(self, username, password, security_answer):
        """
        Initialize a User object with the provided attributes.
        If additional attributes are provided (e.g., from database query),
        they will be ignored to avoid argument mismatches.
        """
        self.username = username
        self.password = self.hash_password(password)
        self.security_answer = self.hash_password(security_answer)
        self.failed_login_attempts = 0
        self.last_login_attempt = None
        self.otp = None
        self.otp_generated_time = None
        self.transactions = []  # List to store user transactions

    @staticmethod
    def hash_password(password):
        """
        Hash the password using SHA-256 for security.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def generate_otp(self):
        """
        Generate a random OTP with a length between OTP_LENGTH_RANGE.
        """
        otp = ''.join(random.choices(string.digits, k=random.randint(*OTP_LENGTH_RANGE)))
        self.otp = self.hash_password(otp)
        self.otp_generated_time = datetime.now()

    def is_otp_expired(self):
        """
        Check if the OTP has expired based on OTP_EXPIRY_TIME.
        """
        if self.otp_generated_time:
            expiry_time = self.otp_generated_time + timedelta(minutes=OTP_EXPIRY_TIME)
            return datetime.now() > expiry_time
        return True

    def reset_failed_login_attempts(self):
        """
        Reset the failed login attempts count to 0.
        """
        self.failed_login_attempts = 0

    def increment_failed_login_attempts(self):
        """
        Increment the failed login attempts count by 1.
        """
        self.failed_login_attempts += 1

    def is_password_valid(self, password):
        """
        Check if the provided password matches the user's password.
        """
        return self.password == self.hash_password(password)

    def is_security_answer_correct(self, answer):
        """
        Check if the provided security answer matches the user's security answer.
        """
        return self.security_answer == self.hash_password(answer)

    def is_account_locked(self):
        """
        Check if the user's account is locked based on MAX_FAILED_LOGIN_ATTEMPTS.
        """
        return self.failed_login_attempts >= MAX_FAILED_LOGIN_ATTEMPTS

    def reset_otp(self):
        """
        Reset the OTP and OTP generation time.
        """
        self.otp = None
        self.otp_generated_time = None

    def add_transaction(self, amount, merchant):
        """
        Add a new transaction to the user's transaction history.
        """
        transaction = {
            "timestamp": datetime.now().isoformat(),
            "amount": amount,
            "merchant": merchant,
        }
        self.transactions.append(transaction)

class MobileBankingApp:
    def __init__(self):
        """
        Initialize the MobileBankingApp with a database connection.
        Create the necessary tables if they don't exist.
        """
        self.db = sqlite3.connect('banking_app.db')
        self.cursor = self.db.cursor()
        self.create_tables()

    def create_tables(self):
        """
        Create the 'users' and 'authentication_logs' tables if they don't exist.
        """
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                security_answer TEXT NOT NULL
            )''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS authentication_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                login_time TEXT NOT NULL,
                success INTEGER NOT NULL,
                otp_used INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )''')
            self.db.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def register_user(self):
        """
        Register a new user by providing a username, password, and security answer.
        Check if the username already exists and throw an error if it does.
        """
        try:
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            security_question = random.choice(list(SECURITY_QUESTIONS.keys()))
            security_answer = input(f"{security_question}: ")
            self.cursor.execute('INSERT INTO users (username, password, security_answer) VALUES (?, ?, ?)', (username, password, security_answer))
            self.db.commit()
            print("Registration successful!")
        except sqlite3.IntegrityError:
            print("Username already exists. Please choose a different username.")
        except sqlite3.Error as e:
            print(f"Error registering user: {e}")

    def login(self):
        """
        Log in a user by providing their username and password.
        Generate an OTP if the credentials are valid and the OTP has expired.
        Prompt the user to enter the OTP to complete the login process.
        Track login attempts and lock the account if the maximum attempts are reached.
        """
        try:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user_data = self.cursor.fetchone()
            if user_data:
                user = User(*user_data)  # Create a User object from the database query result
                if user.is_password_valid(password):
                    if user.is_account_locked():
                        print("Your account is locked. Please contact customer support.")
                        return
                    if user.is_otp_expired():
                        user.generate_otp()
                    else:
                        print(f"Please enter the OTP sent to your registered mobile number (expires in {OTP_EXPIRY_TIME} minutes):")
                        otp = input("OTP: ")
                        if otp == user.otp:
                            user.reset_failed_login_attempts()
                        else:
                            user.increment_failed_login_attempts()
                            if user.is_account_locked():
                                print("Your account is locked. Please contact customer support.")
                                return
                            print("Invalid OTP. Please try again.")
                            return
                    login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    otp_used = otp is not None
                    self.cursor.execute('INSERT INTO authentication_logs (user_id, login_time, success, otp_used) VALUES (?, ?, ?, ?)', (user.id, login_time, True, otp_used))
                    self.db.commit()
                    print("Login successful!")
                else:
                    print("Invalid username or password.")
                    self.cursor.execute('INSERT INTO authentication_logs (user_id, login_time, success, otp_used) VALUES (?, ?, ?, ?)', (user.id, login_time, False, False))
                    self.db.commit()
            else:
                print("User not found.")
        except sqlite3.Error as e:
            print(f"Error logging in: {e}")

    def change_password(self):
        """
        Change a user's password by providing their current password and new password.
        Check if the current password is valid before changing the password.
        """
        try:
            username = input("Enter your username: ")
            user = self.get_user(username)
            if user:
                current_password = input("Enter your current password: ")
                if user.is_password_valid(current_password):
                    new_password = input("Enter your new password: ")
                    user.password = self.hash_password(new_password)
                    self.cursor.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
                    self.db.commit()
                    print("Password changed successfully!")
                else:
                    print("Invalid current password.")
            else:
                print("User not found.")
        except sqlite3.Error as e:
            print(f"Error changing password: {e}")

    def reset_password(self):
        """
        Reset a user's password by answering a security question and providing a new password.
        Check if the security answer is correct before resetting the password.
        """
        try:
            username = input("Enter your username: ")
            user = self.get_user(username)
            if user:
                security_question = random.choice(list(SECURITY_QUESTIONS.keys()))
                print(f"{security_question}:")
                security_answer = input()
                if user.is_security_answer_correct(security_answer):
                    new_password = input("Enter your new password: ")
                    user.password = self.hash_password(new_password)
                    self.cursor.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
                    self.db.commit()
                    print("Password reset successful!")
                else:
                    print("Incorrect security answer.")
            else:
                print("User not found.")
        except sqlite3.Error as e:
            print(f"Error resetting password: {e}")

    def get_user(self, username):
        """
        Get a user by their username from the database.
        Returns a User object if found, otherwise returns None.
        """
        try:
            self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user_data = self.cursor.fetchone()
            if user_data:
                return User(*user_data)  # Create a User object from the database query result
            return None
        except sqlite3.Error as e:
            print(f"Error getting user: {e}")

    def logout(self):
        """
        Log out the current user.
        """