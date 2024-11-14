# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from fastapi.responses import HTMLResponse
# from typing import List
# import asyncio

# app = FastAPI()

# # List to keep track of active WebSocket connections
# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: List[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)
#         print("Client connected")

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)
#         print("Client disconnected")

#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)

# # Initialize the connection manager
# manager = ConnectionManager()

# @app.websocket("/ws/bid")
# async def websocket_endpoint(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             # Broadcasting received bid updates to all clients
#             await manager.broadcast(f"New bid received: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)

# # Sample HTML client for testing
# html = """
# <!DOCTYPE html>
# <html>
# <head>
#     <title>WebSocket Auction System</title>
# </head>
# <body>
#     <h1>Real-Time Auction Bid Updates</h1>
#     <div id="bids"></div>
#     <input type="text" id="bidInput" placeholder="Enter your bid">
#     <button onclick="sendBid()">Submit Bid</button>

#     <script>
#         const ws = new WebSocket("ws://localhost:8000/ws/bid");

#         ws.onmessage = function(event) {
#             const bids = document.getElementById("bids");
#             const message = document.createElement("p");
#             message.textContent = event.data;
#             bids.appendChild(message);
#         };

#         function sendBid() {
#             const input = document.getElementById("bidInput");
#             ws.send(input.value);
#             input.value = '';
#         }
#     </script>
# </body>
# </html>
# """

# @app.get("/")
# async def get():
#     return HTMLResponse(html)






fimport asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Form
from fastapi.responses import HTMLResponse
from typing import List
import sqlite3

app = FastAPI()

# Initialize the SQLite database
conn = sqlite3.connect('auction.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS auction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    minimum_bid REAL NOT NULL,
    current_highest_bid REAL,
    current_highest_bidder TEXT,
    timer INTEGER NOT NULL,
    is_active BOOLEAN NOT NULL CHECK (is_active IN (0, 1))
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS bids (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    auction_id INTEGER NOT NULL,
    bidder TEXT NOT NULL,
    bid_amount REAL NOT NULL,
    FOREIGN KEY (auction_id) REFERENCES auction (id)
)
''')
conn.commit()

# Auction state
auction_state = {
    "minimum_bid": 100,
    "current_highest_bid": 100,
    "current_highest_bidder": None,
    "timer": 60,  # Timer in seconds
    "is_active": True
}

# List to keep track of active WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print("Client connected")
        # Send the current highest bid and timer to the connected client
        await websocket.send_json({
            "type": "initial",
            "bid": auction_state["current_highest_bid"],
            "bidder": auction_state["current_highest_bidder"],
            "timer": auction_state["timer"]
        })

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print("Client disconnected")

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

# Initialize the connection manager
manager = ConnectionManager()

# Retrieve auction details from the database
def get_auction_details():
    cursor.execute('SELECT * FROM auction WHERE is_active = 1')
    return cursor.fetchone()

# Broadcast updated auction details to all clients
async def broadcast_auction_details():
    while True:
        auction_details = get_auction_details()
        if auction_details:
            await manager.broadcast(json.dumps({
                "type": "auction_details",
                "minimum_bid": auction_details[1],
                "current_highest_bid": auction_details[2],
                "current_highest_bidder": auction_details[3],
                "timer": auction_details[4],
                "is_active": auction_details[5]
            }))
        await asyncio.sleep(1)

# Start the auction details broadcast coroutine
asyncio.create_task(broadcast_auction_details())

# WebSocket endpoint for bidding
@app.websocket("/ws/bid")
async def websocket_endpoint(websocket: WebSocket, form: Form):
    await manager.connect(websocket)
    try:
        while auction_state["is_active"]:
            data = await websocket.receive_text()
            # Update the auction state with the new bid
            bid_value = float(data)
            if bid_value > auction_state["current_highest_bid"]:
                auction_state["current_highest_bid"] = bid_value
                auction_state["current_highest_bidder"] = websocket
                # Broadcasting received bid updates to all clients
                await manager.broadcast(f"New highest bid: {bid_value} by {websocket}")
                # Store the bid in the database
                cursor.execute('INSERT INTO bids (auction_id, bidder, bid_amount) VALUES (?, ?, ?)', (1, str(websocket), bid_value))
                conn.commit()
                # Check if the current bidder has been outbid
                if str(websocket) != auction_state["current_highest_bidder"]:
                    await websocket.send_text("You have been outbid!")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Sample HTML client for testing
html = """
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Auction System</title>
</head>
<body>
    <h1>Real-Time Auction Bid Updates</h1>
    <div id="bids"></div>
    <input type="text" id="bidInput" placeholder="Enter your bid">
    <button onclick="sendBid()">Submit Bid</button>

    <script>
        const ws = new WebSocket("ws://localhost:8000/ws/bid");

        ws.onmessage = function(event) {
            const bids = document.getElementById("bids");
            const message = document.createElement("p");
            if (event.data.includes("Time remaining")) {
                document.getElementById("timer").textContent = event.data;
            } else if (event.data.includes("You have been outbid!")) {
                alert(event.data);
            } else {
                message.textContent = event.data;
                bids.appendChild(message);
            }
        };

        function sendBid() {
            const input = document.getElementById("bidInput");
            ws.send(input.value);
            input.value = '';
        }
    </script>
</body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)