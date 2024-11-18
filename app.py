
# from flask import Flask, render_template
# from flask_socketio import SocketIO, emit
# import random
# import time

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app, cors_allowed_origins='*')

# # Simulated energy consumption data
# energy_data = {'consumption': 0}

# # Function to periodically emit energy data to clients
# def update_energy_data():
#     while True:
#         energy_data['consumption'] = random.randint(0, 100)
#         socketio.emit('energy_update', energy_data, to=None)  # Broadcast to all connected clients
#         time.sleep(1)  # Wait for 1 second before updating

# # Start background task for energy data updates
# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')
#     emit('energy_update', energy_data)  # Send initial data
#     socketio.start_background_task(target=update_energy_data)  # Start periodic updates

# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected')

# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == '__main__':
#     socketio.run(app, host='127.0.0.1', port=5000, debug=True)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import time
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*', logging=True, cors_credentials=True)

# Simulated energy consumption data
energy_data = {'consumption': 0}

# Function to simulate energy consumption data updates
def update_energy_data():
    while True:
        energy_data['consumption'] = random.randint(0, 100)
        socketio.emit('energy_update', energy_data)
        time.sleep(1)  # Update data every second

# Create a thread to simulate energy consumption data updates
thread = threading.Thread(target=update_energy_data)
thread.daemon = True  # Set as daemon so it exits when main thread exits

# Render the client HTML template
@app.route('/')
def index():
    thread.start()
    return render_template('index.html')

# Handle client connections
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('energy_update', energy_data)  # Send initial energy consumption data

# Handle client disconnections
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)