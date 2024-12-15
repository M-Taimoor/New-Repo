from celery import Celery
import redis
from redis.exceptions import LockError
from time import sleep
import logging

# Set up logging to display info and error messages
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Celery app with Redis as the broker
app = Celery('ticket_booking', broker='redis://localhost:6379/0')

# Redis client to use for locking
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.task(bind=True)
def book_ticket(self, seat_id):
    """
    Task to book a ticket for a specific seat using a distributed lock.
    """
    lock_key = f"seat_lock:{seat_id}"  # Unique lock for each seat

    try:
        logger.info(f"Attempting to acquire lock for seat {seat_id}...")

        # Try to acquire the lock for the seat with a timeout of 60 seconds
        with redis_client.lock(lock_key, timeout=60):  # Lock for 60 seconds
            logger.info(f"Booking ticket for seat {seat_id}...")
            sleep(5)  # Simulate time taken to complete the booking (e.g., DB transaction)
            logger.info(f"Seat {seat_id} booked successfully.")
    except LockError:
        # If the lock is already held by another task, handle the error
        logger.warning(f"Seat {seat_id} is already being booked. Please try again.")
        raise self.retry(countdown=5)  # Retry the task after 5 seconds if lock not acquired

# Optional: Add result backend configuration (for task results)
app.conf.result_backend = 'redis://localhost:6379/0'
