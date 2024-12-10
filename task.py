from celery import Celery

# Create a Celery instance
app = Celery('my_tasks', broker='redis://localhost:6379/0')

# Define a task
@app.task
def add(x, y):
    return x + y
