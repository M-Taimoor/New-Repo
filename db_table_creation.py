from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Path to the SQLite database file
DATABASE_PATH = 'sqlite:///bank.db'

# Create a database engine
engine = create_engine(DATABASE_PATH, echo=True)

# Declare a base for model classes
Base = declarative_base()

# Define the Account model
class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    balance = Column(Float, nullable=False)

# Create the database and tables
Base.metadata.create_all(engine)

# Create a sessionmaker
Session = sessionmaker(bind=engine)

# Function to create a new account securely
def create_account(name, initial_balance):
    session = Session()
    try:
        new_account = Account(name=name, balance=initial_balance)
        session.add(new_account)
        session.commit()
        return f"Account '{name}' created successfully with balance {initial_balance}"
    except Exception as e:
        session.rollback()
        return f"Error creating account: {e}"
    finally:
        session.close()

# Function to retrieve the balance of an account securely
def get_account_balance(account_name):
    session = Session()
    try:
        account = session.query(Account).filter_by(name=account_name).first()
        if account:
            return f"Account: {account.name}, Balance: {account.balance}"
        else:
            return "Account not found"
    except Exception as e:
        return f"Error retrieving account balance: {e}"
    finally:
        session.close()

# Example usage
if __name__ == "__main__":
    # Create a new account
    print(create_account('John Doe', 1000.0))
    
    # Retrieve the balance for 'John Doe'
    print(get_account_balance('John Doe'))